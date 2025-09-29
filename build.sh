#!/usr/bin/env bash
# Build script para Render
set -o errexit

echo "🚀 Iniciando build para Render..."

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "📊 Ejecutando migraciones..."
python manage.py migrate --settings=smart_condominium.settings.production

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --settings=smart_condominium.settings.production

echo "👥 Creando usuarios predeterminados..."
python manage.py create_default_users --settings=smart_condominium.settings.production

echo "✅ Build completado exitosamente!"