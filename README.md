# Apache Superset Setup Guide

This repository contains the configuration and setup for Apache Superset, a modern data exploration and visualization platform.

## Understanding Superset's Two Databases

Superset uses two different types of databases:

1. **Metadata Database**
   - Purpose: Stores Superset's internal metadata and configurations
   - Content:
     - User information and permissions
     - Dashboard configurations
     - Saved queries
     - Chart definitions
     - Database connections
     - Cache keys
   - Default: SQLite (`superset.db` in project root)
   - Configuration: Set via `SQLALCHEMY_DATABASE_URI` in `superset_config.py`
   - Important Notes:
     - Encryption key (`SUPERSET_SECRET_KEY`) must remain consistent
     - Database credentials are encrypted using this key
     - If key changes, you'll need to reset the database
     - For production, recommended to use PostgreSQL or MySQL

2. **Data Source Databases**
   - Purpose: Store actual data for visualization
   - Types supported:
     - PostgreSQL
     - MySQL
     - SQLite
     - Oracle
     - Microsoft SQL Server
     - Apache Druid
     - StarRocks
     - And many more
   - Configuration Methods:
     - Through Superset's UI (Data → Databases)
     - Via SQLAlchemy URI in configuration
   - Connection Details:
     - Uses SQLAlchemy URI format
     - Credentials encrypted in metadata DB
     - Supports SSH tunneling
     - Can use connection pooling
   - Special Configurations:
     - StarRocks setup requires Docker container
     - Some databases need additional drivers
     - Can configure query timeouts per database

## Prerequisites

- Python 3.10 or higher
- Virtual environment
- Redis (optional, for caching)
- Node.js and npm
- Docker (for StarRocks and other containerized databases)

## Installation Steps

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install apache-superset
```

3. Initialize the database:
```bash
superset db upgrade
```

4. Create an admin user:
```bash
superset fab create-admin
```

5. Load example data:
```bash
superset load_examples
```

## Configuration

### Architecture Overview

- **Frontend Layer**:
  - React-based web interface
  - Visualization plugins
  - Dashboard builder

- **Backend Layer**:
  - Flask application server
  - SQLAlchemy ORM
  - Celery for async tasks
  - Redis for caching

- **Storage Layer**:
  - Metadata database
  - Query results cache
  - Thumbnail cache

### Database Configuration

1. **Metadata Database Configuration**:
```python
# SQLite (default)
SQLALCHEMY_DATABASE_URI = 'sqlite:///path/to/superset.db'

# PostgreSQL (recommended for production)
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/superset'

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/superset'

# Important security settings
SUPERSET_SECRET_KEY = 'your-long-random-string'  # Must be consistent
PREVENT_UNSAFE_DB_CONNECTIONS = True
```

2. **Data Source Database Example Configurations**:
```python
# PostgreSQL
postgresql://user:password@localhost:5432/database

# MySQL
mysql://user:password@localhost:3306/database

# StarRocks
starrocks://user:password@localhost:9030/database

# Additional database parameters
?connect_timeout=10&pool_timeout=30
```

### Storage Configuration

Customize storage locations in `superset_config.py`:

1. **Cache Configuration**:
```python
CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': '/path/to/cache',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24
}
```

2. **Thumbnail Configuration**:
```python
THUMBNAIL_CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': '/path/to/thumbnail_cache'
}
```

3. **Upload Configuration**:
```python
UPLOAD_FOLDER = '/path/to/uploads'
IMG_UPLOAD_FOLDER = '/path/to/image/uploads'
```

## Starting Superset

Use the provided startup script:
```bash
./start_superset.sh
```

Or manually:
```bash
export PYTHONPATH=$PYTHONPATH:$PWD
export SUPERSET_CONFIG_PATH=superset_config.py
source venv/bin/activate
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger
```

## Accessing Superset

- Local access: http://127.0.0.1:8088
- Network access: http://[your-ip]:8088
- Default login: admin/admin

## Troubleshooting

1. Database connection issues:
   - Verify database URI in config
   - Check database permissions
   - For metadata DB encryption issues:
     - Ensure `SUPERSET_SECRET_KEY` is consistent
     - May need to reset the database if key changes
   - For StarRocks:
     - Ensure Docker container is running
     - Check container logs for connection issues

2. Cache issues:
   - Ensure cache directories are writable
   - Clear cache directories if needed

3. Visualization problems:
   - Check browser console for errors
   - Verify required dependencies

## Additional Resources

- [Apache Superset Documentation](https://superset.apache.org/docs/intro)
- [Superset GitHub Repository](https://github.com/apache/superset)
- [StarRocks Documentation](https://docs.starrocks.io/)