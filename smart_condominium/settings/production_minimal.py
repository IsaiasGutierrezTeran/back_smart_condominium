"""
Configuración minimalista para producción en Render
"""
from .base import *
import os
import dj_database_url

# Configuración básica para producción
DEBUG = False
ALLOWED_HOSTS = ['*']  # Permitir todos los hosts temporalmente

# Database para producción
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }

# Static files con WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CORS básico
CORS_ALLOW_ALL_ORIGINS = True

# Logging completamente deshabilitado
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
    },
}

# Email básico
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'