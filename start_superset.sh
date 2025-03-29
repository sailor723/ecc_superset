#!/bin/bash

echo "Superset Startup Script"
echo "======================="
echo

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Check and start PostgreSQL container
echo "Checking PostgreSQL container..."
if ! docker ps --format '{{.Names}}' | grep -q "^superset-postgres$"; then
    echo "Starting PostgreSQL container..."
    docker start superset-postgres || {
        echo "Creating new PostgreSQL container..."
        docker run --name superset-postgres \
            -e POSTGRES_PASSWORD=superset \
            -e POSTGRES_USER=superset \
            -e POSTGRES_DB=superset \
            -p 5432:5432 \
            -d postgres:14
    }
else
    echo "superset-postgres is already running"
fi
echo "Waiting for superset-postgres to initialize..."
sleep 5

# Check and start MySQL container
echo "Checking MySQL container..."
if ! docker ps --format '{{.Names}}' | grep -q "^superset-mysql$"; then
    echo "Starting MySQL container..."
    docker start superset-mysql || {
        echo "Creating new MySQL container..."
        docker run --name superset-mysql \
            -e MYSQL_ROOT_PASSWORD=superset \
            -e MYSQL_DATABASE=superset \
            -e MYSQL_USER=superset \
            -e MYSQL_PASSWORD=superset \
            -p 3306:3306 \
            -d mysql:latest \
            --character-set-server=utf8mb4 \
            --collation-server=utf8mb4_unicode_ci \
            --max_allowed_packet=128M
    }
else
    echo "superset-mysql is already running"
fi
echo "Waiting for superset-mysql to initialize..."
sleep 5

# Configure MySQL
echo "Configuring MySQL for file uploads..."
MYSQL_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' superset-mysql)
echo "MySQL container IP: $MYSQL_IP"

# Configure MySQL user
echo "Updating MySQL user permissions..."
docker exec -i superset-mysql mysql -uroot -psuperset << EOF
CREATE USER IF NOT EXISTS 'superset'@'%' IDENTIFIED BY 'superset';
GRANT ALL PRIVILEGES ON *.* TO 'superset'@'%' WITH GRANT OPTION;
CREATE DATABASE IF NOT EXISTS test_schema;
USE test_schema;
CREATE TABLE IF NOT EXISTS test_table (id INT, name VARCHAR(100));
FLUSH PRIVILEGES;
SET GLOBAL max_connections = 500;
SET GLOBAL interactive_timeout = 300;
SET GLOBAL wait_timeout = 300;
EOF
echo "MySQL user permissions updated."

# Check if port 8088 is in use
if check_port 8088; then
    echo "Port 8088 is already in use. Please manually free the port and try again."
    exit 1
fi

# Clean temporary files
echo "Cleaning temporary files..."
rm -rf /tmp/superset_uploads/* 2>/dev/null
mkdir -p /tmp/superset_uploads/
chmod 777 /tmp/superset_uploads/

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup_superset.sh first."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$PWD
export FLASK_APP=superset
export FLASK_ENV=development
export SUPERSET_CONFIG_PATH=$PWD/superset_config.py

# Optional memory limits to prevent crashes
export PYTHONMALLOC=malloc
export MALLOC_TRIM_THRESHOLD_=65536
export PYTHONWARNINGS=ignore

# Make sure upload directory exists
mkdir -p /tmp/superset_uploads/
chmod 777 /tmp/superset_uploads/

# Start Superset
echo -e "\n===== MySQL Connection Info for UI Setup ====="
echo "MySQL IP: $MYSQL_IP"
echo "Username: superset"
echo "Password: superset"
echo "Database: superset"
echo "Port: 3306"
echo "==========================================="

echo -e "\nStarting Superset server..."
echo "Access URL: http://localhost:8088"
echo "Default credentials: admin/admin"

python fix_superset.py run -p 8088 --with-threads --reload