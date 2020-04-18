from .base import *

DEBUG = True
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
MEDIA_URL = os.environ.get('GS_BUCKET_URL')
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATIC_ROOT = '/var/www/html/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DATABASE_URL = 'postgresql:///postgresql'
import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)