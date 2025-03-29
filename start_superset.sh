#!/bin/bash

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Function to kill existing Superset processes
kill_superset() {
    echo "Stopping any running Superset processes..."
    pkill -f "superset run" || true
    sleep 2
}

# Function to check if a container exists
container_exists() {
    local container_name=$1
    if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
        return 0
    else
        return 1
    fi
}

# Function to check if a container is running
container_running() {
    local container_name=$1
    if docker ps --format '{{.Names}}' | grep -q "^$container_name$"; then
        return 0
    else
        return 1
    fi
}

# Function to handle container
handle_container() {
    local container_name=$1
    local image=$2
    local port=$3
    local env_vars=$4

    if container_running "$container_name"; then
        echo "$container_name is already running"
    elif container_exists "$container_name"; then
        echo "Starting existing $container_name container..."
        docker start "$container_name"
    else
        echo "Creating and starting new $container_name container..."
        docker run --name "$container_name" \
            $env_vars \
            -p $port \
            -d $image
    fi
    
    # Wait for container to be fully started
    echo "Waiting for $container_name to initialize..."
    sleep 5
}

# Check and start PostgreSQL container
echo "Checking PostgreSQL container..."
handle_container "superset-postgres" "postgres:14" \
    "5432:5432" \
    "-e POSTGRES_PASSWORD=superset -e POSTGRES_USER=superset -e POSTGRES_DB=superset"

# Check and start MySQL container
echo "Checking MySQL container..."
handle_container "superset-mysql" "mysql:latest" \
    "3306:3306" \
    "-e MYSQL_ROOT_PASSWORD=superset -e MYSQL_DATABASE=superset -e MYSQL_USER=superset -e MYSQL_PASSWORD=superset"

# Configure MySQL for file uploads
echo "Configuring MySQL for file uploads..."
sleep 5  # Wait for MySQL to fully initialize

# Get the MySQL container IP
MYSQL_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' superset-mysql)
echo "MySQL container IP: $MYSQL_IP"

# Configure MySQL permissions - add proper grants for the superset user
if docker exec -i superset-mysql mysql -uroot -psuperset -e "SELECT 1" > /dev/null 2>&1; then
    echo "Updating MySQL user permissions..."
    docker exec -i superset-mysql mysql -uroot -psuperset << EOF
ALTER USER 'superset'@'%' IDENTIFIED BY 'superset'; 
GRANT ALL PRIVILEGES ON *.* TO 'superset'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF
    echo "MySQL user permissions updated."
else
    echo "Warning: Could not connect to MySQL server. User permissions not updated."
fi

# Kill any existing Superset processes
kill_superset

# Check if port 8088 is in use
if check_port 8088; then
    echo "Port 8088 is already in use. Please free up the port and try again."
    exit 1
fi

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please create it first."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$PWD
export FLASK_APP=superset
export FLASK_ENV=development
export SUPERSET_CONFIG_PATH=$PWD/superset_config.py

# Make sure upload directory exists and has proper permissions
mkdir -p /tmp/superset_uploads/
chmod 777 /tmp/superset_uploads/

# Create fixed Superset launcher if it doesn't exist
if [ ! -f "fix_superset.py" ]; then
    echo "Creating fixed Superset launcher..."
    cat > fix_superset.py << PYFILE
#!/usr/bin/env python
from superset.cli.main import superset
if __name__ == "__main__":
    superset()
PYFILE
    chmod +x fix_superset.py
fi

# Start Superset
echo "Starting Superset server..."
echo "Access URL: http://localhost:8088"
echo "Default credentials: admin/admin"

# Run Superset with proper error handling
python fix_superset.py run -p 8088 --with-threads --reload || {
    echo "Failed to start Superset. Check the error messages above."
    exit 1
}