import os
from datetime import timedelta
from flask_appbuilder.security.manager import AUTH_DB

# Flask App Builder configuration
APP_NAME = "ECC Superset"
APP_ICON = "/static/assets/images/superset-logo-horiz.png"
APP_HOME = "/superset/welcome/"

# Superset timeout
SUPERSET_WEBSERVER_TIMEOUT = 300

# The SQLAlchemy connection string to the PostgreSQL database
SQLALCHEMY_DATABASE_URI = 'postgresql://superset:superset@localhost:5432/superset'

# Setup Redis for caching
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_CELERY_DB = 0
REDIS_RESULTS_DB = 1

# Cache
CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp/superset_cache',
    'CACHE_DEFAULT_TIMEOUT': 86400,  # 24 hours
}

# Results backend - using Redis
RESULTS_BACKEND = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_KEY_PREFIX': 'superset_results',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_DB': REDIS_RESULTS_DB,
}

# File uploads configuration
UPLOAD_FOLDER = '/tmp/superset_uploads/'
CSV_UPLOAD_FOLDER = '/tmp/superset_uploads/'

# Configure web server
ENABLE_PROXY_FIX = True
WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = ['superset.views.core.log']
MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY', '')

# Feature flags
FEATURE_FLAGS = {
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_NATIVE_FILTERS_SET': True,
    'EMBEDDED_SUPERSET': True,
    'TAGGING_SYSTEM': True,
    'DASHBOARD_CACHE': True,
    'DASHBOARD_RBAC': True,
    'DYNAMIC_PLUGINS': True,
    'SCHEDULED_QUERIES': True,
    'SQL_VALIDATORS_BY_ENGINE': True,
    'ALERT_REPORTS': True,
}

# Configure auth
AUTH_TYPE = AUTH_DB
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"

# Configure session parameters
PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
SESSION_COOKIE_SAMESITE = None

# Configure connections to data sources
ADDITIONAL_MIDDLEWARE = []

# MySQL Database Connections
PREFERRED_DATABASES = [
    'mysql',
    'postgresql',
    'sqlite',
]

# Example database connection string templates for MySQL
SQLALCHEMY_EXAMPLES_URI = 'mysql://superset:superset@localhost:3306/superset'

# Configure MySQL for example datasets
EXAMPLES_USER = 'superset'
EXAMPLES_PASSWORD = 'superset'
EXAMPLES_HOST = 'localhost'
EXAMPLES_PORT = 3306
EXAMPLES_DB = 'superset'

# Configure custom query templates
SQL_MAX_ROW = 100000
SQL_ASYNC_TIME_LIMIT_SEC = 300

# Configure languages
BABEL_DEFAULT_LOCALE = 'en'
LANGUAGES = {
    'en': {'flag': 'us', 'name': 'English'},
}

# Email configuration
SMTP_HOST = os.environ.get('SMTP_HOST', 'localhost')
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PORT = os.environ.get('SMTP_PORT', 25)
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
SMTP_MAIL_FROM = os.environ.get('SMTP_MAIL_FROM', 'superset@superset.com')

# Druid
DRUID_TZ = 'UTC'
DRUID_ANALYSIS_TYPES = ['cardinality']

# Dashboard position and sizes configuration
DASHBOARD_POSITION_DATA_LIMIT = 65535
DASHBOARD_FILTERS_EXPERIMENTAL_UI = True