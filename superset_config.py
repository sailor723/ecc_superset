from flask_appbuilder.security.manager import AUTH_DB
import os

# Superset specific config
ROW_LIMIT = 5000

FEATURE_FLAGS = {"EMBEDDED_SUPERSET": True}

# Generate a secure random key
SECRET_KEY = "PPbnGCaGjzdWQ8zuYm5aIc35+iSZ36fggIh/1V+wpIcs3ZGbCLZfux4v"

# The SQLAlchemy connection string
SQLALCHEMY_DATABASE_URI = "postgresql://superset:superset@localhost:5432/superset"

# Secret key used for encrypting sensitive data
SUPERSET_SECRET_KEY = "3e76e023dff4061db3d1d5dd88597d91"

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True

# Cache configuration
CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 86400,
}

# Thumbnail cache configuration
THUMBNAIL_CACHE_CONFIG = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "/tmp/superset_thumbnails",
}

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY", "")

# File upload configuration
UPLOAD_FOLDER = "/tmp/superset_uploads/"
IMG_UPLOAD_FOLDER = "/tmp/superset_uploads/images"

# Additional configuration settings
CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = ["superset.views.core.log"]
SUPERSET_WEBSERVER_TIMEOUT = 300

# Authentication config
AUTH_TYPE = AUTH_DB

# Whether to run the web server in debug mode or not
DEBUG = True

# Flask App Builder configuration
FAB_API_SWAGGER_UI = True

# A dictionary of Frontend package versions
FRONTEND_PACKAGE_VERSIONS = {"apache-superset": "4.1.2"}

# JWT token for async queries
JWT_SECRET = "3e76e023dff4061db3d1d5dd88597d91"
JWT_COOKIE_NAME = "async-token"
JWT_COOKIE_SECURE = False

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
    "SQLLAB_BACKEND_PERSISTENCE": False,
    "UPLOAD_EXTENSION": True,
    "ENABLE_TEMPLATE_REMOVAL": True,
    "DASHBOARD_RBAC": True,
    "EMBEDDED_SUPERSET": True,
    "ENABLE_EXPLORE_JSON_CSRF_PROTECTION": False,
    "DASHBOARD_FILTERS_EXPERIMENTAL": True,
    "GLOBAL_ASYNC_QUERIES": False,
    "ENABLE_ASYNC_QUERY_MANAGER": False,
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

# Enable CORS
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "resources": ["*"],
    "origins": ["*"],
}

# Upload settings
UPLOAD_FOLDER = "/tmp/superset_uploads/"
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100MB
UPLOAD_CHUNK_SIZE = 4096

# Enable SQL Lab
SQLLAB_ENABLED = True
SQLLAB_ASYNC_TIME_LIMIT_SEC = 60
SQL_MAX_ROW = 10000
SQL_QUERY_MUTATING_THRESHOLD_DURATION = 60
SQLLAB_TIMEOUT = 60
SQLLAB_VALIDATION_TIMEOUT = 30
RESULTS_BACKEND_USE_MSGPACK = False
CELERY_CONFIG = {}

# Set proper memory limits
DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 60 * 60,  # 1 hour cache
    "CACHE_THRESHOLD": 500,  # Maximum items in cache
}

# Force queries to be run synchronously in SQL Lab
GLOBAL_ASYNC_QUERIES_JWT_ENABLED = False
ENABLE_ASYNC_QUERY_MANAGER = False

# Basic config
APP_NAME = "ECC Superset"
APP_ICON = "/static/assets/images/superset-logo-horiz.png"

# Configure auth
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set proper file permissions for upload directory
try:
    os.chmod(UPLOAD_FOLDER, 0o777)
except:
    pass
