# 🏢 Smart Condominium - AWS Deployment Guide

Guía completa para desplegar Smart Condominium en Amazon Web Services.

## 🚀 Requisitos Previos

### 1. Instancia EC2
- **OS:** Ubuntu 22.04 LTS
- **Tipo:** t3.medium (mínimo) o t3.large (recomendado)
- **Almacenamiento:** 20GB SSD (mínimo)
- **Security Groups:**
  - SSH (22): Tu IP
  - HTTP (80): 0.0.0.0/0
  - HTTPS (443): 0.0.0.0/0
  - Custom (8000): 0.0.0.0/0

## 📋 Pasos de Instalación Rápida

### 1. Conectar a la instancia
```bash
ssh -i tu-clave.pem ubuntu@tu-ip-publica
```

### 2. Ejecutar script automático
```bash
# Instalar Docker
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu
sudo apt install docker-compose -y

# Configurar SWAP si es necesario
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Reiniciar
sudo reboot
```

### 3. Clonar y desplegar
```bash
# Después del reinicio
git clone https://github.com/IsaiasGutierrezTeran/back_smart_condominium.git
cd back_smart_condominium

# Configurar
cp .env.aws .env
nano .env  # Editar variables

# Desplegar
chmod +x deploy.sh
./deploy.sh
```

## 🔐 Usuarios Automáticos

| Usuario | Contraseña | Email |
|---------|------------|-------|
| `admin` | `admin123` | admin@smartcondo.com |
| `demo.residente` | `demo123` | demo@smartcondo.com |
| `demo.seguridad` | `security123` | seguridad@smartcondo.com |

## 🌐 Acceso
- **Admin:** `http://tu-ip:8000/admin/`
- **API:** `http://tu-ip:8000/api/`