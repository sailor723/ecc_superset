# Apache Superset Setup Guide

This repository contains the configuration and setup for Apache Superset, a modern data exploration and visualization platform.

## Prerequisites

- Python 3.10 or higher
- Virtual environment
- Redis (optional, for caching)
- Node.js and npm

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

### Storage Locations

1. **Metadata Storage**:
   - Default SQLite database (`superset.db`) in project root
   - Contains user info, dashboards, saved queries, and database connections

2. **Visualization Storage**:
   - Charts configuration in metadata DB
   - Custom plugins in `superset-frontend/plugins/`
   - Generated thumbnails in `/tmp/superset_thumbnails/`

3. **Query Storage**:
   - Saved queries in metadata DB
   - Query results cache in DB/Redis

4. **Asset Storage**:
   - Static assets in application directories
   - Uploaded files in configured upload directory

### Storage Configuration

Customize storage locations in `superset_config.py`:

1. **Metadata Database**:
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///path/to/superset.db'
# or
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/superset'
```

2. **Cache Configuration**:
```python
CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': '/path/to/cache',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24
}
```

3. **Thumbnail Configuration**:
```python
THUMBNAIL_CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': '/path/to/thumbnail_cache'
}
```

4. **Upload Configuration**:
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

2. Cache issues:
   - Ensure cache directories are writable
   - Clear cache directories if needed

3. Visualization problems:
   - Check browser console for errors
   - Verify required dependencies

## Additional Resources

- [Apache Superset Documentation](https://superset.apache.org/docs/intro)
- [Superset GitHub Repository](https://github.com/apache/superset)