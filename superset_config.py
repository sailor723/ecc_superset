from flask_appbuilder.security.manager import AUTH_DB
import os

# The secret key for signing stuff
SECRET_KEY = "PPbnGCaGjzdWQ8zuYm5aIc35+iSZ36fggIh/1V+wpIcs3ZGbCLZfux4v"

# JWT token for async queries
JWT_SECRET = "PPbnGCaGjzdWQ8zuYm5aIc35+iSZ36fggIh/1V+wpIcs3ZGbCLZfux4v"
JWT_COOKIE_NAME = "async-token"
JWT_COOKIE_SECURE = False

# The SQLAlchemy connection string for PostgreSQL (metadata database)
SQLALCHEMY_DATABASE_URI = "postgresql://superset:superset@localhost:5432/superset"

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = [
    "superset.views.core.log",
    "superset.charts.api.data",
    "superset.datasets.api.data",
    "superset.datasets.api.import_",
    "superset.datasets.api.upload",
    "superset.databases.api.connect",
    "superset.databases.api.upload_csv",
    "superset.databases.api.upload_excel",
    "superset.databases.api.import_",
    "superset.views.database.views.upload_csv",
    "superset.views.database.views.upload_excel",
    "superset.views.database.api.*",
    "superset.datasets.api.*",
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
    "supports_credentials": True,
    "allow_headers": ["*"],
    "resources": ["*"],
    "origins": ["*"],
}

# Upload settings
UPLOAD_FOLDER = "/tmp/superset_uploads/"
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100MB
UPLOAD_CHUNK_SIZE = 4096

# Database configurations
DATABASES = {
    "mysql": {
        "allow_file_upload": True,
        "allowed_extensions": {"csv", "xlsx", "xls", "parquet"},
        "csv_extensions": {"csv"},
        "excel_extensions": {"xlsx", "xls"},
        "engine": "mysql",
        "port": 3306,
        "allow_csv_upload": True,
        "allow_ctas": True,
        "allow_cvas": True,
        "allow_dml": True,
        "expose_in_sqllab": True,
        "allow_multi_schema_metadata_fetch": True,
        "allow_file_upload": True,
        "extra": {"ssl": False},
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
GLOBAL_ASYNC_QUERIES_JWT_SECRET = (
    "PPbnGCaGjzdWQ8zuYm5aIc35+iSZ36fggIh/1V+wpIcs3ZGbCLZfux4v"
)
