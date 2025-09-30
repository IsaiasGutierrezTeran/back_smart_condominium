"""
Configuración minimalista para producción en Render
"""
from .base import *
import os
import dj_database_url

# Configuración básica para producción
DEBUG = False
ALLOWED_HOSTS = ['*']  # Permitir todos los hosts temporalmente

# Database para producción - Usar DATABASE_URL de Render
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Usar la base de datos de Render
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback - no debería usarse en producción
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'condominiobd',
            'USER': 'postgres',
            'PASSWORD': '250203is',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

print(f"DATABASE_URL disponible: {'Sí' if DATABASE_URL else 'No'}")
if DATABASE_URL:
    print(f"Usando base de datos de Render")
else:
    print(f"Usando base de datos local (fallback)")

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