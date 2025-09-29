#!/bin/bash

# Script de despliegue para AWS
# Ejecutar: ./deploy_aws.sh

echo "🚀 Iniciando despliegue en AWS..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Crear archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --settings=smart_condominium.settings.production

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate --settings=smart_condominium.settings.production

# Crear superusuario si no existe
echo "👤 Configurando usuario administrador..."
python manage.py shell --settings=smart_condominium.settings.production << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@condominio.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('Superusuario ya existe')
EOF

# Verificar configuración
echo "✅ Verificando configuración..."
python manage.py check --settings=smart_condominium.settings.production

echo "🎉 Despliegue completado!"
echo ""
echo "📋 Información importante:"
echo "   - Backend URL: https://your-app.elasticbeanstalk.com"
echo "   - Admin Panel: https://your-app.elasticbeanstalk.com/admin/"
echo "   - API Base: https://your-app.elasticbeanstalk.com/api/"
echo ""
echo "🔗 Endpoints principales:"
echo "   - Autenticación: /api/auth/"
echo "   - Finanzas: /api/finanzas/"  
echo "   - Comunicación: /api/comunicacion/"
echo "   - Reservas: /api/reservas/"
echo "   - Seguridad: /api/seguridad/"
echo "   - Mantenimiento: /api/mantenimiento/"
echo ""
echo "📱 Configurar en React/Flutter:"
echo "   const API_BASE_URL = 'https://your-app.elasticbeanstalk.com/api';"