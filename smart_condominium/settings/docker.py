"""
Configuración específica para Docker testing
"""

from .base import *
import os

# DEBUG
DEBUG = True

# Base de datos para Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smart_condominium_test',
        'USER': 'postgres',
        'PASSWORD': 'postgres123',
        'HOST': 'db_simple',
        'PORT': '5432',
        'OPTIONS': {
            # Sin SSL para Docker local
        },
    }
}

# Redis para Docker
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis_simple:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de email para testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Seguridad para testing
ALLOWED_HOSTS = ['*']

# CORS para testing
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# JWT settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Logging
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
        'level': 'INFO',
    },
}

print("🐳 Configuración Docker cargada")
print(f"   DATABASE: {DATABASES['default']['NAME']}@{DATABASES['default']['HOST']}")
print(f"   REDIS: {CACHES['default']['LOCATION']}")
print(f"   DEBUG: {DEBUG}")