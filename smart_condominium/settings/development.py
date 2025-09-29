"""
Configuración para desarrollo
"""
from .base import *

# Debug para desarrollo
DEBUG = True

# Hosts permitidos para desarrollo
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Base de datos para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'condominiobd',
        'USER': 'postgres',
        'PASSWORD': '250203is',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Configuración adicional para desarrollo
CORS_ALLOW_ALL_ORIGINS = True

# Logging para desarrollo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}
