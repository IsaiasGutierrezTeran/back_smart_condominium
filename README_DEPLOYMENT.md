# 🚀 Smart Condominium - Despliegue en AWS

Backend optimizado para React y Flutter con despliegue en AWS.

## 📋 Características del Backend

### ✅ **APIs REST Completas**
- **Autenticación**: JWT con refresh tokens
- **Finanzas**: Pagos, expensas, reportes
- **Comunicación**: Avisos, notificaciones
- **Reservas**: Áreas comunes, gestión de reservas
- **Seguridad**: IA facial, OCR placas, incidentes
- **Mantenimiento**: Solicitudes, seguimiento

### ✅ **Optimizado para Producción AWS**
- Configuración para Elastic Beanstalk
- Soporte para RDS PostgreSQL
- Integración con S3 para archivos
- WhiteNoise para archivos estáticos
- Gunicorn como servidor WSGI
- Docker y Docker Compose incluidos

### ✅ **Compatibilidad Frontend**
- **React**: APIs REST con CORS configurado
- **Flutter**: Serialización JSON optimizada
- **Autenticación**: Token JWT estándar
- **Documentación**: Endpoints documentados

---

## 🛠️ Configuración de Desarrollo

### 1. **Configuración Local**
```bash
# Clonar repositorio
git clone <repo-url>
cd smart-condominium

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python manage.py migrate --settings=smart_condominium.settings.development

# Crear superusuario
python manage.py createsuperuser --settings=smart_condominium.settings.development

# Ejecutar servidor
python manage.py runserver --settings=smart_condominium.settings.development
```

### 2. **Con Docker**
```bash
# Construir y ejecutar
docker-compose up --build

# Acceder a:
# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin/
# API: http://localhost:8000/api/
```

---

## 🚀 Despliegue en AWS

### **Opción 1: Elastic Beanstalk (Recomendado)**

1. **Preparar aplicación:**
```bash
# Instalar EB CLI
pip install awsebcli

# Inicializar aplicación
eb init smart-condominium

# Crear entorno
eb create smart-condominium-prod
```

2. **Configurar variables de entorno:**
```bash
# Configurar en AWS Console o via CLI
eb setenv DJANGO_SETTINGS_MODULE=smart_condominium.settings.production
eb setenv SECRET_KEY=your-secret-key
eb setenv DB_HOST=your-rds-endpoint.amazonaws.com
eb setenv DB_NAME=condominium_prod
eb setenv DB_USER=postgres
eb setenv DB_PASSWORD=your-password
```

3. **Desplegar:**
```bash
eb deploy
```

### **Opción 2: EC2 con Docker**

1. **Configurar EC2:**
```bash
# Conectar a EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Instalar Docker
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo usermod -aG docker ubuntu
```

2. **Desplegar aplicación:**
```bash
# Clonar código
git clone <repo-url>
cd smart-condominium

# Configurar variables
cp .env.production .env
# Editar .env con valores reales

# Ejecutar
docker-compose up -d
```

### **Opción 3: ECS/Fargate**

1. **Construir imagen:**
```bash
# Build y push a ECR
docker build -t smart-condominium .
docker tag smart-condominium:latest your-account.dkr.ecr.region.amazonaws.com/smart-condominium:latest
docker push your-account.dkr.ecr.region.amazonaws.com/smart-condominium:latest
```

2. **Configurar ECS Service con la imagen**

---

## 🗄️ Base de Datos

### **RDS PostgreSQL (Producción)**
```sql
-- Crear base de datos
CREATE DATABASE condominium_prod;
CREATE USER condominium_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE condominium_prod TO condominium_user;
```

### **Migraciones**
```bash
# Ejecutar migraciones en producción
python manage.py migrate --settings=smart_condominium.settings.production

# Datos iniciales
python manage.py loaddata initial_data.json --settings=smart_condominium.settings.production
```

---

## 📡 Integración con Frontend

### **React.js**
```javascript
// src/config/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// src/services/authService.js
import axios from 'axios';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: (email, password) => 
    api.post('/auth/login/', { email, password }),
  
  getProfile: () => 
    api.get('/auth/profile/'),
  
  // Otros métodos...
};
```

### **Flutter**
```dart
// lib/services/api_service.dart
import 'package:dio/dio.dart';

class ApiService {
  static const String baseUrl = 'https://your-app.elasticbeanstalk.com/api';
  
  final Dio _dio = Dio(BaseOptions(
    baseUrl: baseUrl,
    headers: {'Content-Type': 'application/json'},
  ));

  // Constructor con interceptor JWT
  ApiService() {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        final token = getStoredToken(); // Implementar
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
    ));
  }

  // Métodos de autenticación
  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await _dio.post('/auth/login/', data: {
      'email': email,
      'password': password,
    });
    return response.data;
  }

  // Otros métodos...
}
```

---

## 🔒 Seguridad

### **Variables de Entorno Críticas**
```bash
# Generar SECRET_KEY seguro
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Configurar en AWS Systems Manager Parameter Store
aws ssm put-parameter \
  --name "/smart-condominium/SECRET_KEY" \
  --value "your-generated-secret-key" \
  --type "SecureString"
```

### **Configuración HTTPS**
```bash
# En Elastic Beanstalk, configurar Load Balancer con certificado SSL
# O usar CloudFront con certificado ACM
```

---

## 📊 Monitoreo

### **CloudWatch Logs**
- Logs de aplicación en `/var/log/django/`
- Métricas de performance
- Alertas automáticas

### **Health Checks**
```python
# Endpoint de health check
GET /api/health/
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

---

## 🚀 URLs de Producción

Una vez desplegado, las URLs serán:

### **Backend APIs**
```
https://your-app.elasticbeanstalk.com/api/auth/      # Autenticación
https://your-app.elasticbeanstalk.com/api/finanzas/ # Finanzas
https://your-app.elasticbeanstalk.com/api/comunicacion/ # Comunicación
https://your-app.elasticbeanstalk.com/api/reservas/     # Reservas
https://your-app.elasticbeanstalk.com/api/seguridad/    # Seguridad
https://your-app.elasticbeanstalk.com/api/mantenimiento/ # Mantenimiento
```

### **Panel de Administración**
```
https://your-app.elasticbeanstalk.com/admin/
```

---

## 📋 Checklist de Despliegue

- [ ] Variables de entorno configuradas
- [ ] Base de datos RDS creada
- [ ] S3 bucket para media files (opcional)
- [ ] Certificado SSL configurado
- [ ] CORS origins actualizados
- [ ] DNS configurado (si usas dominio personalizado)
- [ ] Monitoring y logs configurados
- [ ] Backup automático de BD configurado

---

## 🆘 Solución de Problemas

### **Error: Database Connection**
```bash
# Verificar variables de entorno
eb config

# Verificar conectividad a RDS
telnet your-rds-endpoint.amazonaws.com 5432
```

### **Error: Static Files**
```bash
# Recolectar archivos estáticos
python manage.py collectstatic --settings=smart_condominium.settings.production
```

### **Error: CORS**
```python
# Verificar en settings/production.py
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
]
```

---

## 📞 Soporte

Para problemas específicos:
1. Revisar logs en CloudWatch
2. Verificar configuración en AWS Console
3. Testear endpoints con Postman
4. Verificar variables de entorno

**¡Tu backend está listo para React y Flutter en AWS!** 🎉