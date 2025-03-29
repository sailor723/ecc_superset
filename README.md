# Apache Superset Setup for ECC

This repository provides a streamlined setup for Apache Superset with PostgreSQL and MySQL databases, including necessary configuration for ECC data visualization needs.

## Prerequisites

- Python 3.10 (specifically 3.10, not newer versions)
- Docker
- Bash shell (Linux or WSL on Windows)

## Quick Start

The setup process has been automated with scripts. Follow these simple steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/sailor723/ecc_superset.git
   cd ecc_superset
   ```

2. Make the scripts executable:
   ```bash
   chmod +x setup_superset.sh start_superset.sh
   ```

3. Run the setup script:
   ```bash
   ./setup_superset.sh
   ```

4. Start Superset:
   ```bash
   ./start_superset.sh
   ```

5. Access Superset at: http://localhost:8088
   - Default login: admin/admin

## What the Setup Does

The setup script automatically:
- Creates a Python 3.10 virtual environment
- Installs Apache Superset and all dependencies
- Sets up PostgreSQL container for main Superset metadata
- Sets up MySQL container for datasets and examples
- Configures database permissions for file uploads
- Initializes Superset with admin user and example datasets
- Creates necessary configuration files

## Manual Setup (Alternative)

If you prefer to set up manually, follow these steps:

### 1. Setup Environment and Install Superset

```bash
# Create Python virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install Superset and dependencies
pip install apache-superset
pip install psycopg2-binary pymysql
```

### 2. Set Up Databases with Docker

```bash
# Start PostgreSQL
docker run --name superset-postgres \
  -e POSTGRES_PASSWORD=superset \
  -e POSTGRES_USER=superset \
  -e POSTGRES_DB=superset \
  -p 5432:5432 \
  -d postgres:14

# Start MySQL
docker run --name superset-mysql \
  -e MYSQL_ROOT_PASSWORD=superset \
  -e MYSQL_DATABASE=superset \
  -e MYSQL_USER=superset \
  -e MYSQL_PASSWORD=superset \
  -p 3306:3306 \
  -d mysql:latest

# Configure MySQL permissions
docker exec -i superset-mysql mysql -uroot -psuperset << EOF
ALTER USER 'superset'@'%' IDENTIFIED BY 'superset';
GRANT ALL PRIVILEGES ON *.* TO 'superset'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF
```

### 3. Create Configuration File

Create a file named `superset_config.py` with the configuration included in this repository.

### 4. Initialize Superset

```bash
# Set up environment variables
export PYTHONPATH=$PYTHONPATH:$PWD
export FLASK_APP=superset
export FLASK_ENV=development
export SUPERSET_CONFIG_PATH=$PWD/superset_config.py

# Initialize the database
superset db upgrade

# Create an admin user
superset fab create-admin \
   --username admin \
   --firstname Admin \
   --lastname User \
   --email admin@example.com \
   --password admin

# Load examples
superset load_examples

# Initialize
superset init
```

### 5. Start Superset

```bash
superset run -p 8088 --with-threads --reload
```

## Troubleshooting

If you encounter any issues:

1. **Python Version**: Ensure you're using Python 3.10 exactly.
   ```bash
   python --version
   ```

2. **Docker Services**: Verify Docker containers are running.
   ```bash
   docker ps
   ```

3. **Port Conflicts**: Check if ports 8088, 5432, or 3306 are already in use.
   ```bash
   lsof -i :8088
   lsof -i :5432
   lsof -i :3306
   ```

4. **Log Files**: Check Superset logs in the terminal for error messages.

5. **Configuration**: Ensure your superset_config.py file is correctly set up and readable.

## Custom Data Sources

To connect to custom data sources:
1. Log in to Superset
2. Go to Data → Databases
3. Click "+ Database"
4. Select your database type
5. Configure the connection parameters

## Maintenance

To update Superset to the latest version:
1. Stop any running instance
2. Activate the virtual environment
3. Run `pip install --upgrade apache-superset`
4. Run `superset db upgrade`
5. Restart Superset

## License

This setup repository is provided under the Apache License 2.0.
Apache Superset is a product of the Apache Software Foundation.