#!/bin/bash

# Esperar que la base de datos esté disponible
echo "Esperando que la base de datos esté disponible..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
    echo "Base de datos no disponible, esperando..."
    sleep 2
done

echo "Base de datos disponible, ejecutando migraciones..."

# Ejecutar migraciones
python manage.py migrate --noinput

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Cargar datos iniciales (usuarios predeterminados)
echo "Cargando datos iniciales..."
python manage.py create_default_users

echo "Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 --max-requests 1000 --max-requests-jitter 100 smart_condominium.wsgi:application