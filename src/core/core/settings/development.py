"""Module contains development configurations for the app."""
from .base import *

DEBUG = True
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT= os.path.join(BASE_DIR, 'media/')
MEDIA_URL= "/media/"