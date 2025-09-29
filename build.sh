# Build script para Render
#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate --settings=smart_condominium.settings.production

# Recolectar archivos estáticos
python manage.py collectstatic --noinput --settings=smart_condominium.settings.production

# Crear usuarios predeterminados
python manage.py create_default_users --settings=smart_condominium.settings.production