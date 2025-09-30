#!/usr/bin/env bash
# Build script para Render
set -o errexit

echo "Starting build for Render..."

# Verificar Python y pip
echo "Python version: $(python --version)"
echo "pip version: $(pip --version)"

echo "Updating pip..."
python -m pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

# Verificar instalación de Django
echo "Verifying Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Verificar variables de entorno
echo "Checking environment variables..."
echo "DATABASE_URL set: $(if [ -n "$DATABASE_URL" ]; then echo 'YES'; else echo 'NO'; fi)"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"

# Verificar configuraciones
echo "Verifying Django configuration..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_condominium.settings.production_minimal')
import django
django.setup()
from django.conf import settings
print('Django configuration loaded successfully')
print(f'DEBUG: {settings.DEBUG}')
print(f'DATABASES configured: {len(settings.DATABASES)}')
print(f'Database ENGINE: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
if 'HOST' in settings.DATABASES['default']:
    print(f'Database HOST: {settings.DATABASES[\"default\"][\"HOST\"]}')
"

echo "Running migrations..."
python manage.py migrate --settings=smart_condominium.settings.production_minimal

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=smart_condominium.settings.production_minimal

echo "Creating default users..."
python manage.py create_default_users --settings=smart_condominium.settings.production_minimal || echo "Warning: Could not create default users"

echo "Build completed successfully!"