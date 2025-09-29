# Guía de Despliegue Smart Condominium en AWS
# ==============================================

## PASO 1: Crear instancia EC2
1. Ir a AWS Console > EC2
2. Crear instancia Ubuntu 22.04 LTS
3. Tipo: t3.medium (mínimo para Docker)
4. Configurar Security Groups:
   - SSH (22): Tu IP
   - HTTP (80): 0.0.0.0/0
   - HTTPS (443): 0.0.0.0/0
   - Custom (8000): 0.0.0.0/0 (Django)
   - Custom (5432): Solo desde la VPC (PostgreSQL)

## PASO 2: Conectar a la instancia
```bash
ssh -i tu-clave.pem ubuntu@tu-ip-publica
```

## PASO 3: Configurar el servidor (ejecutar en orden)
```bash
# 1. Convertirse en super usuario
sudo su

# 2. Actualizar paquetes
sudo apt update
sudo apt upgrade -y

# 3. Instalar paquetes necesarios
sudo apt install ca-certificates curl gnupg lsb-release -y

# 4. Agregar clave GPG de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 5. Agregar repositorio de Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 6. Instalar Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# 7. Instalar Docker Compose
sudo apt install docker-compose -y

# 8. Agregar usuario ubuntu al grupo docker
sudo usermod -aG docker ubuntu

# 9. Reiniciar para aplicar cambios
sudo reboot
```

## PASO 4: Configurar memoria SWAP (si es necesario)
```bash
# Verificar memoria
free -h

# Si necesitas más memoria, crear SWAP
sudo fallocate -l 2G /swapfile
# Si falla usar: sudo dd if=/dev/zero of=/swapfile bs=1M count=2048

sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
swapon --show
```

## PASO 5: Clonar el proyecto
```bash
# Clonar tu repositorio
git clone https://github.com/IsaiasGutierrezTeran/back_smart_condominium.git
cd back_smart_condominium

# Cambiar a la rama correcta
git checkout main
git pull origin main
```

## PASO 6: Configurar variables de entorno
```bash
# Crear archivo .env
nano .env
```

## PASO 7: Desplegar con Docker
```bash
# Crear red de backend
docker network create backend

# Opción 1: Si tienes archivos separados
docker-compose -f docker-compose.db.yml up -d
docker-compose -f docker-compose.app.yml up --build

# Opción 2: Si usas un solo archivo
docker-compose up --build -d
```

## COMANDOS DE MANTENIMIENTO

### Limpiar y reconstruir
```bash
docker-compose down --volumes --rmi all
docker system prune -af --volumes
docker-compose up --build -d
```

### Acceder a contenedores
```bash
docker exec -it <nombre_contenedor> /bin/bash
```

### Verificar logs
```bash
docker-compose logs -f web
```