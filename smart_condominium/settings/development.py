"""
Configuración para desarrollo
"""
from .base import *
from decouple import config

# Debug para desarrollo
DEBUG = True

# Hosts permitidos para desarrollo
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Base de datos para desarrollo - usando variables de entorno
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='condominiobd'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='250203is'),
        'HOST': config('DB_HOST', default='localhost'),  # localhost para desarrollo local
        'PORT': config('DB_PORT', default='5432'),
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
