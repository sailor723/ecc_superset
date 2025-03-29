#!/bin/bash

echo "Superset Setup Script"
echo "====================="
echo

# Check if Python 3.10 is installed
if ! command -v python3.10 &> /dev/null; then
    echo "Python 3.10 is required but not installed. Please install Python 3.10 first."
    exit 1
fi

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Docker is required but not installed. Please install Docker first."
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Do you want to recreate it? (y/n)"
    read -r recreate_venv
    if [[ $recreate_venv == "y" ]]; then
        echo "Removing existing virtual environment..."
        rm -rf venv
    else
        echo "Using existing virtual environment."
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python 3.10 virtual environment..."
    python3.10 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please check your Python installation."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Failed to upgrade pip. Continuing anyway..."
fi

# Install Python packages
echo "Installing required Python packages..."

# Install with constraints file
if [ -f "requirements-local.txt" ]; then
    echo "Installing from requirements-local.txt..."
    pip install -r requirements-local.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install from requirements-local.txt."
        exit 1
    fi
else
    # Install Apache Superset
    echo "Installing Apache Superset..."
    pip install apache-superset
    if [ $? -ne 0 ]; then
        echo "Failed to install Apache Superset."
        exit 1
    fi
    
    # Install required drivers
    echo "Installing database drivers..."
    pip install psycopg2-binary pymysql
    if [ $? -ne 0 ]; then
        echo "Failed to install database drivers."
        exit 1
    fi
    
    # Save requirements to file
    echo "Saving requirements to requirements-local.txt..."
    pip freeze > requirements-local.txt
fi

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$PWD
export FLASK_APP=superset
export FLASK_ENV=development
export SUPERSET_CONFIG_PATH=$PWD/superset_config.py

# Create directories for Superset
echo "Creating directories for Superset..."
mkdir -p /tmp/superset_uploads/
mkdir -p /tmp/superset_cache/
chmod 777 /tmp/superset_uploads/
chmod 777 /tmp/superset_cache/

# Start PostgreSQL container if it doesn't exist
echo "Setting up PostgreSQL container..."
if ! docker ps -a --format '{{.Names}}' | grep -q "^superset-postgres$"; then
    echo "Creating PostgreSQL container..."
    docker run --name superset-postgres \
        -e POSTGRES_PASSWORD=superset \
        -e POSTGRES_USER=superset \
        -e POSTGRES_DB=superset \
        -p 5432:5432 \
        -d postgres:14
else
    echo "PostgreSQL container already exists."
    if ! docker ps --format '{{.Names}}' | grep -q "^superset-postgres$"; then
        echo "Starting PostgreSQL container..."
        docker start superset-postgres
    else
        echo "PostgreSQL container is already running."
    fi
fi

# Start MySQL container if it doesn't exist
echo "Setting up MySQL container..."
if ! docker ps -a --format '{{.Names}}' | grep -q "^superset-mysql$"; then
    echo "Creating MySQL container..."
    docker run --name superset-mysql \
        -e MYSQL_ROOT_PASSWORD=superset \
        -e MYSQL_DATABASE=superset \
        -e MYSQL_USER=superset \
        -e MYSQL_PASSWORD=superset \
        -p 3306:3306 \
        -d mysql:latest
else
    echo "MySQL container already exists."
    if ! docker ps --format '{{.Names}}' | grep -q "^superset-mysql$"; then
        echo "Starting MySQL container..."
        docker start superset-mysql
    else
        echo "MySQL container is already running."
    fi
fi

echo "Waiting for databases to initialize..."
sleep 10

# Make sure superset_config.py exists
if [ ! -f "superset_config.py" ]; then
    echo "superset_config.py not found. Please make sure it exists before continuing."
    exit 1
fi

# Configure MySQL permissions
echo "Configuring MySQL permissions..."
docker exec -i superset-mysql mysql -uroot -psuperset << EOF
ALTER USER 'superset'@'%' IDENTIFIED BY 'superset';
GRANT ALL PRIVILEGES ON *.* TO 'superset'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

# Initialize Superset database
echo "Initializing Superset database..."
superset db upgrade
if [ $? -ne 0 ]; then
    echo "Failed to initialize Superset database. Creating fixed launcher..."
    # Create a fixed launcher for Superset
    cat > fix_superset.py << PYFILE
#!/usr/bin/env python
from superset.cli.main import superset
if __name__ == "__main__":
    superset()
PYFILE
    chmod +x fix_superset.py
    
    # Try again with fixed launcher
    echo "Retrying database initialization with fixed launcher..."
    python fix_superset.py db upgrade
    if [ $? -ne 0 ]; then
        echo "Failed to initialize Superset database."
        exit 1
    fi
else
    # Create a fixed launcher for Superset anyway for consistency
    cat > fix_superset.py << PYFILE
#!/usr/bin/env python
from superset.cli.main import superset
if __name__ == "__main__":
    superset()
PYFILE
    chmod +x fix_superset.py
fi

# Create Superset admin user
echo "Creating Superset admin user..."
python fix_superset.py fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com \
    --password admin
if [ $? -ne 0 ]; then
    echo "Failed to create admin user."
    exit 1
fi

# Load examples
echo "Loading example data..."
python fix_superset.py load_examples
if [ $? -ne 0 ]; then
    echo "Failed to load example data. Continuing anyway..."
fi

# Initialize roles
echo "Initializing roles..."
python fix_superset.py init
if [ $? -ne 0 ]; then
    echo "Failed to initialize roles."
    exit 1
fi

# Make superset_config readable
chmod +r superset_config.py

# Make the start script executable
chmod +x start_superset.sh

echo
echo "Superset setup complete!"
echo "========================="
echo "You can now start Superset by running: ./start_superset.sh"
echo "Access Superset at: http://localhost:8088"
echo "Default credentials: admin/admin"
echo