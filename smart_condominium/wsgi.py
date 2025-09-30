"""
WSGI config for smart_condominium project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Configurar el settings module para producción en Render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_condominium.settings.production')

application = get_wsgi_application()
