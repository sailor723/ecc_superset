# Superset specific config
ROW_LIMIT = 5000

# Flask App Builder configuration
SECRET_KEY = '\x02\xf2w\xf9\x0f\x96\xb6\xc4\xf0\xb3k\xdf\xd2\x01\xf9\xd3\x8e\xdd\xbe\x9c\xb5\x81@\xd6\x01\x1c\x00\xf9'

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': '/tmp/superset_cache',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,  # 1 day default cache timeout
}

# Thumbnail cache configuration
THUMBNAIL_CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': '/tmp/superset_thumbnails',
}

# File upload configuration
UPLOAD_FOLDER = '/tmp/superset_uploads'
IMG_UPLOAD_FOLDER = '/tmp/superset_uploads/images'

# Additional configuration settings
WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = ['superset.views.core.log']
SUPERSET_WEBSERVER_TIMEOUT = 300