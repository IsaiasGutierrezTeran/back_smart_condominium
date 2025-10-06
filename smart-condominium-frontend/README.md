# Smart Condominium Frontend

Sistema Integral de Gestión para Condominios Inteligentes - Aplicación Frontend desarrollada en React.

## 🏢 Descripción

Smart Condominium es una aplicación web moderna y responsive que permite gestionar de manera integral todas las operaciones de un condominio inteligente. Incluye módulos para finanzas, comunicación, reservas, seguridad y mantenimiento.

## ✨ Características Principales

- **🎨 Diseño UX/UI Profesional**: Interfaz moderna con Material-UI y animaciones fluidas
- **👥 Roles de Usuario**: Dashboard personalizado para Administradores, Residentes, Seguridad y Mantenimiento
- **📱 Responsive Design**: Optimizado para dispositivos móviles, tablets y desktop
- **🔐 Autenticación JWT**: Sistema de autenticación seguro con refresh tokens
- **🚀 Performance**: Optimizado con React Query para cache y gestión de estado
- **♿ Accesibilidad**: Cumple con estándares de accesibilidad web

## 🛠️ Stack Tecnológico

### Dependencias Principales
- **React 18.2.0** - Biblioteca principal de UI
- **Material-UI 5.11.0** - Componentes de diseño
- **React Router 6.8.0** - Enrutamiento
- **Axios 1.3.0** - Cliente HTTP
- **React Query 4.24.0** - Gestión de estado del servidor
- **Framer Motion 10.0.0** - Animaciones
- **React Hook Form 7.43.0** - Gestión de formularios
- **Date-fns 2.29.0** - Manejo de fechas
- **Recharts 2.5.0** - Gráficos y visualizaciones
- **JWT Decode 3.1.2** - Decodificación de tokens JWT

## 🚀 Instalación y Configuración

### Prerrequisitos
- Node.js 16+ 
- npm o yarn
- Acceso al backend de Smart Condominium

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd smart-condominium-frontend
```

2. **Instalar dependencias**
```bash
npm install
# o
yarn install
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
```

Editar el archivo `.env` con las configuraciones apropiadas:
```env
REACT_APP_API_BASE_URL=https://back-smart-condominium-1.onrender.com
REACT_APP_ENVIRONMENT=production
REACT_APP_VERSION=1.0.0
REACT_APP_COMPANY_NAME=Smart Condominium
```

4. **Ejecutar en modo desarrollo**
```bash
npm start
# o
yarn start
```

La aplicación estará disponible en `http://localhost:3000`

5. **Construir para producción**
```bash
npm run build
# o
yarn build
```

## 👥 Usuarios de Prueba

La aplicación incluye usuarios de prueba para diferentes roles:

| Rol | Usuario | Contraseña | Descripción |
|-----|---------|------------|-------------|
| Administrador | `admin` | `admin123` | Acceso completo a todos los módulos |
| Residente | `demo.residente` | `demo123` | Acceso a servicios de residente |
| Seguridad | `demo.seguridad` | `security123` | Acceso al módulo de seguridad |

## 📁 Estructura del Proyecto

```
smart-condominium-frontend/
├── public/                 # Archivos públicos
├── src/
│   ├── assets/            # Recursos estáticos
│   ├── components/        # Componentes React
│   │   ├── auth/         # Componentes de autenticación
│   │   ├── common/       # Componentes comunes
│   │   ├── dashboard/    # Dashboards por rol
│   │   ├── finance/      # Componentes de finanzas
│   │   ├── communication/ # Componentes de comunicación
│   │   ├── reservations/ # Componentes de reservas
│   │   ├── security/     # Componentes de seguridad
│   │   └── maintenance/  # Componentes de mantenimiento
│   ├── contexts/         # Contextos de React
│   ├── hooks/            # Hooks personalizados
│   ├── pages/            # Páginas de la aplicación
│   ├── services/         # Servicios de API
│   ├── theme/            # Configuración del tema
│   ├── utils/            # Utilidades
│   └── App.js            # Componente principal
├── package.json
└── README.md
```

## 🎯 Módulos de la Aplicación

### 1. **Dashboard**
- Dashboard personalizado según el rol del usuario
- Métricas en tiempo real
- Accesos rápidos
- Notificaciones importantes

### 2. **Finanzas**
- Gestión de pagos y cuotas
- Historial de transacciones
- Reportes financieros
- Estados de cuenta

### 3. **Comunicación**
- Noticias del condominio
- Avisos y anuncios
- Sistema de notificaciones
- Centro de mensajes

### 4. **Reservas**
- Reserva de espacios comunes
- Calendario de disponibilidad
- Gestión de reservas
- Confirmaciones automáticas

### 5. **Seguridad**
- Control de visitantes
- Gestión vehicular
- Registro de incidentes
- Funciones de IA (Reconocimiento facial, OCR)

### 6. **Mantenimiento**
- Solicitudes de mantenimiento
- Seguimiento de trabajos
- Reportes de estado
- Gestión de técnicos

## 🔐 Sistema de Autenticación

El sistema utiliza JWT (JSON Web Tokens) para la autenticación:

- **Access Token**: Para autenticación de requests (24 horas)
- **Refresh Token**: Para renovar el access token (7 días)
- **Auto-refresh**: Renovación automática de tokens
- **Protección de rutas**: Rutas protegidas según roles de usuario

## 🎨 Tema y Diseño

### Paleta de Colores
- **Primario**: #1565C0 (Azul corporativo)
- **Secundario**: #FFC107 (Amarillo dorado)
- **Éxito**: #2E7D32 (Verde)
- **Advertencia**: #F57C00 (Naranja)
- **Error**: #C62828 (Rojo)

### Tipografía
- **Principal**: Inter (encabezados)
- **Secundaria**: Roboto (cuerpo de texto)

## 📱 Responsive Design

La aplicación está optimizada para:
- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px  
- **Desktop**: 1024px+

## 🔧 Scripts Disponibles

```bash
# Desarrollo
npm start              # Inicia el servidor de desarrollo
npm test               # Ejecuta las pruebas
npm run build          # Construye la aplicación para producción
npm run lint           # Ejecuta el linter
npm run lint:fix       # Corrige errores de linting automáticamente
npm run format         # Formatea el código con Prettier
```

## 🌐 API Backend

La aplicación se conecta al backend de Smart Condominium:
- **URL Base**: https://back-smart-condominium-1.onrender.com
- **Documentación**: Disponible en el repositorio backend
- **Tecnología**: Django + PostgreSQL

## 📊 Características Técnicas

### Performance
- **Code Splitting**: Carga lazy de componentes
- **Memoización**: Optimización de re-renders
- **Cache**: Gestión inteligente con React Query
- **Bundle Size**: Optimizado para carga rápida

### Seguridad
- **HTTPS**: Comunicación segura
- **Token Management**: Gestión segura de tokens
- **Input Validation**: Validación de formularios
- **Error Boundaries**: Manejo de errores

### Accesibilidad
- **ARIA Labels**: Etiquetas para lectores de pantalla
- **Keyboard Navigation**: Navegación por teclado
- **Color Contrast**: Contraste adecuado
- **Focus Management**: Gestión de foco

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico:
- **Email**: soporte@smartcondominium.com
- **Documentación**: Ver carpeta `/docs`
- **Issues**: Crear un issue en GitHub

## 🚀 Deployment

### Vercel (Recomendado)
```bash
npm install -g vercel
vercel --prod
```

### Netlify
```bash
npm run build
# Subir carpeta build/ a Netlify
```

### Docker
```bash
docker build -t smart-condominium-frontend .
docker run -p 3000:3000 smart-condominium-frontend
```

---

**Smart Condominium Frontend v1.0.0**  
Desarrollado con ❤️ para la gestión inteligente de condominios.