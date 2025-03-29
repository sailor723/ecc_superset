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

Create a file named `superset_config.py` with the necessary configuration for Superset.

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

# Initialize
superset init
```

## 5. Start Superset

Run the startup script:
```bash
./start_superset.sh
```

## 6. Access Superset

- Access Superset at http://localhost:8088
- Login with username `admin` and password `admin`