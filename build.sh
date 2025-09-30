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

# Verificar configuraciones
echo "Verifying Django configuration..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_condominium.settings.production')
import django
django.setup()
from django.conf import settings
print('Django configuration loaded successfully')
print(f'DEBUG: {settings.DEBUG}')
print(f'DATABASES configured: {len(settings.DATABASES)}')
"

echo "Running migrations..."
python manage.py migrate --settings=smart_condominium.settings.production

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=smart_condominium.settings.production

echo "Creating default users..."
python manage.py create_default_users --settings=smart_condominium.settings.production || echo "Warning: Could not create default users"

echo "Build completed successfully!"