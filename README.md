# Apache Superset Setup Guide

This guide provides step-by-step instructions for setting up Apache Superset with PostgreSQL and MySQL databases, enabling file uploads and configuring all necessary components.

## Prerequisites

- Python 3.10
- Docker
- Bash shell

## 1. Setup Environment and Install Superset

```bash
# Create Python virtual environment
python -m venv venv
source venv/bin/activate

# Install Superset and dependencies
pip install apache-superset
pip install psycopg2-binary mysqlclient
```

## 2. Set Up Databases with Docker

The included startup script will automatically handle this for you. It will:
- Create and start PostgreSQL container if it doesn't exist
- Create and start MySQL container if it doesn't exist
- Configure the necessary permissions

## 3. Create Superset Configuration File

Create a file named `superset_config.py` with the following content:

```python
from flask_appbuilder.security.manager import AUTH_DB
import os

# The secret key for signing stuff
SECRET_KEY = "your_secure_key_here"

# JWT token for async queries
JWT_SECRET = "your_secure_key_here"
JWT_COOKIE_NAME = "async-token"
JWT_COOKIE_SECURE = False

# The SQLAlchemy connection string for PostgreSQL (metadata database)
SQLALCHEMY_DATABASE_URI = "postgresql://superset:superset@localhost:5432/superset"

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = [
    'superset.views.core.log', 
    'superset.charts.api.data', 
    'superset.datasets.api.data',
    'superset.datasets.api.import_',
    'superset.datasets.api.upload',
    'superset.databases.api.connect',
    'superset.databases.api.upload_csv', 
    'superset.databases.api.upload_excel',
    'superset.databases.api.import_',
    'superset.views.database.views.upload_csv',
    'superset.views.database.views.upload_excel',
    'superset.views.database.api.*',
    'superset.datasets.api.*',
]
WTF_CSRF_TIME_LIMIT = None

# Add this for serving on localhost
ENABLE_PROXY_FIX = True

# File upload settings
ALLOWED_FILE_EXTENSIONS = {"csv", "xlsx", "xls", "parquet"}
UPLOAD_FOLDER = "/tmp/superset_uploads/"
FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "ALLOW_FULL_CSV_EXPORT": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ENABLE_JAVASCRIPT_CONTROLS": True,
    "VERSIONED_EXPORT": True,
    "GENERIC_CHART_AXES": True,
    "DYNAMIC_PLUGINS": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "ENABLE_EXPLORE_DRAG_AND_DROP": True,
    "ENABLE_DND_WITH_CLICK_UX": True,
    "ENABLE_ADVANCED_DATA_TYPES": True,
    "SQLLAB_BACKEND_PERSISTENCE": True,
    "UPLOAD_EXTENSION": True,
    "ENABLE_TEMPLATE_REMOVAL": True,
    "DASHBOARD_RBAC": True,
    "EMBEDDED_SUPERSET": True,
    "ENABLE_EXPLORE_JSON_CSRF_PROTECTION": False,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_FILTERS_EXPERIMENTAL": True,
    "GLOBAL_ASYNC_QUERIES": True,
    "ENABLE_ASYNC_QUERY_MANAGER": True,
    "ALERT_REPORTS_NOTIFICATION_DRY_RUN": True,
    "ENABLE_JAVASCRIPT_CONTROLS": True,
}

# Enable file upload for database
ENABLE_UPLOAD_DB = True
PREVENT_UNSAFE_DB_CONNECTIONS = False
CSV_ALLOWED_EXTENSIONS = {"csv"}
EXCEL_ALLOWED_EXTENSIONS = {"xlsx", "xls"}
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "parquet"}

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Enable database query sharing in Superset
ENABLE_JAVASCRIPT_CONTROLS = True
ENABLE_TEMPLATE_PROCESSING = True

# Additional database engines
ADDITIONAL_ENGINES = True
PREFERRED_DATABASES = ["postgresql", "mysql"]

# Enable CORS
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['*']
}

# Upload settings
UPLOAD_FOLDER = "/tmp/superset_uploads/"
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100MB
UPLOAD_CHUNK_SIZE = 4096

# Database configurations
DATABASES = {
    'mysql': {
        'allow_file_upload': True,
        'allowed_extensions': {"csv", "xlsx", "xls", "parquet"},
        'csv_extensions': {"csv"},
        'excel_extensions': {"xlsx", "xls"},
        'engine': 'mysql',
        'port': 3306,
        'allow_csv_upload': True,
        'allow_ctas': True,
        'allow_cvas': True,
        'allow_dml': True,
        'expose_in_sqllab': True,
        'allow_multi_schema_metadata_fetch': True,
        'allow_file_upload': True,
        'extra': {
            'ssl': False
        }
    }
}

# MySQL specific settings
SQLALCHEMY_CUSTOM_PASSWORD_STORE = None
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_MAX_OVERFLOW = 10

# Enable SQL Lab
SQLLAB_ENABLED = True
SQLLAB_ASYNC_TIME_LIMIT_SEC = 300
SQL_MAX_ROW = 100000
SQL_QUERY_MUTATING_THRESHOLD_DURATION = 3600
SQLLAB_TIMEOUT = 30
SQLLAB_VALIDATION_TIMEOUT = 10

# Security settings
TALISMAN_ENABLED = False
ENABLE_PROXY_FIX = True
ENABLE_CORS = True

# File upload settings
UPLOAD_EXTENSION = True
UPLOAD_FOLDER = "/tmp/superset_uploads/"
IMG_UPLOAD_FOLDER = "/tmp/superset_uploads/"

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set proper file permissions for upload directory
try:
    os.chmod(UPLOAD_FOLDER, 0o777)
except:
    pass

# Additional settings
FILTER_STATE_CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 86400,
    "CACHE_THRESHOLD": 500,
}

# Async Query settings
GLOBAL_ASYNC_QUERIES_JWT_ENABLED = True
GLOBAL_ASYNC_QUERIES_JWT_COOKIE_NAME = "async-token"
GLOBAL_ASYNC_QUERIES_JWT_COOKIE_SECURE = False
GLOBAL_ASYNC_QUERIES_JWT_SECRET = "your_secure_key_here"
```

## 4. Initialize Superset

```bash
# Set up environment variables
export PYTHONPATH=$PYTHONPATH:$PWD
export FLASK_APP=superset

# Initialize the database
superset db upgrade

# Create an admin user
superset fab create-admin \
   --username admin \
   --firstname admin \
   --lastname admin \
   --email admin@localhost \
   --password admin

# Load examples (optional)
superset load_examples

# Initialize
superset init
```

## 5. Configure Database for File Uploads

Create a script named `update_db.py` to ensure all database settings allow file uploads:

```python
# update_db.py
import psycopg2
import json
from psycopg2.extras import RealDictCursor

# Get PostgreSQL connection details
pg_uri = "postgresql://superset:superset@localhost:5432/superset"

# Connect to PostgreSQL
conn = psycopg2.connect(pg_uri)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Get all databases
cursor.execute("SELECT id, database_name, extra FROM dbs")
databases = cursor.fetchall()

# Update each database
for db in databases:
    print(f"Updating database: {db['database_name']}")
    
    # Parse extra JSON
    try:
        extra = json.loads(db['extra']) if db['extra'] else {}
    except json.JSONDecodeError:
        extra = {}
    
    # Update extra configuration
    extra.update({
        "allows_virtual_table_explore": True,
        "allow_multi_schema_metadata_fetch": True,
        "allow_csv_upload": True,
    })
    
    # Update database settings
    cursor.execute(
        """
        UPDATE dbs 
        SET 
            allow_file_upload = TRUE, 
            allow_ctas = TRUE,
            allow_cvas = TRUE,
            allow_dml = TRUE,
            extra = %s
        WHERE id = %s
        """,
        (json.dumps(extra), db['id'])
    )

# Commit changes
conn.commit()
cursor.close()
conn.close()

print(f"Updated {len(databases)} databases to allow file uploads")
```

Run the script:
```bash
python update_db.py
```

## 6. Create Startup Script

Create a file named `start_superset.sh` with the following content:

```bash
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
    sudo pkill -f "superset run" || true
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

# Start Superset
echo "Starting Superset server..."
echo "Access URL: http://localhost:8088"
echo "Default credentials: admin/admin"

# Run Superset with proper error handling
superset run -p 8088 --with-threads --reload || {
    echo "Failed to start Superset. Check the error messages above."
    exit 1
}
```

Make the script executable:
```bash
chmod +x start_superset.sh
```

## 7. Start Superset

Run the startup script:
```bash
./start_superset.sh
```

## 8. Access Superset

- Access Superset at http://localhost:8088
- Login with username `admin` and password `admin`

## 9. Usage Guide

### Upload Files to MySQL
1. Go to **Data → Datasets → + Dataset**
2. Select MySQL as your database
3. Choose "Upload a file" and select your CSV or Excel file
4. Configure your table settings and click "Save"

### Create Queries in SQL Lab
1. Go to **SQL Lab → SQL Editor**
2. Select MySQL from the database dropdown
3. Choose "superset" schema
4. Write SQL queries to explore your data
5. Use the "Run" button to execute queries

### Create Visualizations
1. Create a query in SQL Lab
2. Click "Explore" to visualize the results
3. Choose a visualization type
4. Save your visualization as a chart

### Create Dashboards
1. Go to **Dashboards → + Dashboard**
2. Add charts to your dashboard
3. Arrange and resize charts as needed
4. Save your dashboard

## 10. Troubleshooting

### MySQL Connection Issues
If you have trouble connecting to MySQL, make sure:
1. The container is running (`docker ps | grep superset-mysql`)
2. The IP address is correct (check with `docker inspect superset-mysql`)
3. The MySQL user has the right permissions
4. When connecting in Superset, use the container's IP address (usually 172.17.0.2 or similar)

### File Upload Issues
If file uploads aren't working:
1. Run the `update_db.py` script to ensure database settings are correct
2. Ensure the `ALLOWED_EXTENSIONS` in `superset_config.py` is using set syntax: `{"csv", "xlsx"}`
3. Check that the upload directory exists and has proper permissions
4. Verify the MySQL user has appropriate privileges with: `GRANT ALL PRIVILEGES ON *.* TO 'superset'@'%' WITH GRANT OPTION;`

### Starting Containers
The startup script will automatically handle container management, but if you need to manually manage containers:
```bash
# List containers
docker ps -a

# Start containers individually
docker start superset-postgres superset-mysql

# Get container IPs
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' superset-mysql
``` 