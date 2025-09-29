#!/bin/bash

# Script de instalación automática de Docker en Ubuntu
# ====================================================

echo "🐳 INSTALANDO DOCKER EN UBUNTU"
echo "==============================="

# 1. Actualizar sistema
echo "📦 Actualizando paquetes del sistema..."
sudo apt update
sudo apt upgrade -y

# 2. Instalar paquetes necesarios
echo "🔧 Instalando dependencias..."
sudo apt install ca-certificates curl gnupg lsb-release -y

# 3. Agregar clave GPG de Docker
echo "🔐 Configurando repositorio de Docker..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Agregar repositorio de Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Instalar Docker
echo "🐳 Instalando Docker..."
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# 6. Instalar Docker Compose
echo "🔧 Instalando Docker Compose..."
sudo apt install docker-compose -y

# 7. Agregar usuario al grupo docker
echo "👤 Configurando permisos de usuario..."
sudo usermod -aG docker $USER
sudo usermod -aG docker ubuntu

# 8. Configurar SWAP si hay poca memoria
echo "💾 Verificando memoria del sistema..."
MEMORY=$(free -m | awk '/^Mem:/{print $2}')
if [ $MEMORY -lt 2048 ]; then
    echo "⚠️  Memoria baja detectada ($MEMORY MB). Configurando SWAP..."
    
    if [ ! -f /swapfile ]; then
        sudo fallocate -l 2G /swapfile
        sudo chmod 600 /swapfile
        sudo mkswap /swapfile
        sudo swapon /swapfile
        
        # Hacer permanente
        echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
        
        echo "✅ SWAP de 2GB configurado"
    else
        echo "ℹ️  SWAP ya existe"
    fi
else
    echo "✅ Memoria suficiente ($MEMORY MB)"
fi

# 9. Verificar instalación
echo "🔍 Verificando instalación..."
docker --version
docker-compose --version

# 10. Mensaje final
echo ""
echo "🎉 ¡DOCKER INSTALADO EXITOSAMENTE!"
echo "=================================="
echo ""
echo "📋 Próximos pasos:"
echo "   1. Reiniciar la sesión: exit && ssh ..."
echo "   2. O reiniciar el servidor: sudo reboot"
echo "   3. Verificar: docker run hello-world"
echo ""
echo "⚠️  IMPORTANTE: Debes cerrar y volver a conectar por SSH"
echo "   para que los cambios de grupo tomen efecto."
echo ""

# Preguntar si quiere reiniciar
read -p "¿Quieres reiniciar el servidor ahora? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Reiniciando servidor..."
    sudo reboot
fi