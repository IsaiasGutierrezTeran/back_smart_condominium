#!/bin/bash

# Script de despliegue automático para Smart Condominium en AWS
# ==============================================================

echo "🚀 INICIANDO DESPLIEGUE DE SMART CONDOMINIUM EN AWS"
echo "==================================================="

# Verificar si estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encuentra manage.py. Asegúrate de estar en el directorio del proyecto."
    exit 1
fi

# 1. Actualizar código desde Git
echo "📥 Actualizando código desde Git..."
git pull origin main

# 2. Verificar que existe el archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  No se encuentra .env. Copiando desde .env.aws..."
    cp .env.aws .env
fi

# 3. Crear red de Docker si no existe
echo "🌐 Creando red de Docker..."
docker network create backend 2>/dev/null || echo "Red backend ya existe"

# 4. Parar contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose -f docker-compose.app.yml down
docker-compose -f docker-compose.db.yml down

# 5. Limpiar imágenes y volúmenes antiguos (opcional)
read -p "¿Quieres limpiar imágenes y volúmenes antiguos? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Limpiando imágenes y volúmenes antiguos..."
    docker system prune -af --volumes
fi

# 6. Construir y levantar base de datos
echo "🗄️  Levantando base de datos..."
docker-compose -f docker-compose.db.yml up -d

# 7. Esperar que la base de datos esté lista
echo "⏳ Esperando que la base de datos esté lista..."
sleep 10

# 8. Construir y levantar aplicación
echo "🏗️  Construyendo y levantando aplicación..."
docker-compose -f docker-compose.app.yml up --build -d

# 9. Verificar estado de los contenedores
echo "📊 Verificando estado de los contenedores..."
docker-compose -f docker-compose.app.yml ps
docker-compose -f docker-compose.db.yml ps

# 10. Mostrar logs de la aplicación
echo "📝 Mostrando logs de la aplicación..."
docker-compose -f docker-compose.app.yml logs web --tail=20

echo ""
echo "🎉 ¡DESPLIEGUE COMPLETADO!"
echo "========================"
echo ""
echo "📋 URLs disponibles:"
echo "   🌐 Aplicación: http://$(curl -s ifconfig.me):8000"
echo "   ⚙️  Admin: http://$(curl -s ifconfig.me):8000/admin/"
echo "   🔧 Nginx: http://$(curl -s ifconfig.me)"
echo ""
echo "🔐 Usuarios predeterminados:"
echo "   👨‍💼 admin / admin123"
echo "   🏠 demo.residente / demo123"
echo "   🛡️  demo.seguridad / security123"
echo ""
echo "📱 Comandos útiles:"
echo "   Ver logs: docker-compose -f docker-compose.app.yml logs -f"
echo "   Reiniciar: docker-compose -f docker-compose.app.yml restart"
echo "   Acceder a contenedor: docker exec -it smart_condo_web /bin/bash"