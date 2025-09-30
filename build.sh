#!/usr/bin/env bash
# Build script para Render
set -o errexit

echo "🚀 Iniciando build para Render..."

# Verificar Python y pip
echo "� Python version: $(python --version)"
echo "�📦 pip version: $(pip --version)"

echo "📦 Actualizando pip..."
python -m pip install --upgrade pip

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Verificar instalación de Django
echo "🔍 Verificando instalación de Django..."
python -c "import django; print(f'Django version: {django.get_version()}')"

echo "📊 Ejecutando migraciones..."
python manage.py migrate --settings=smart_condominium.settings.production

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --settings=smart_condominium.settings.production

echo "👥 Creando usuarios predeterminados..."
python manage.py create_default_users --settings=smart_condominium.settings.production

echo "✅ Build completado exitosamente!"