# 🚀 Smart Condominium - Despliegue en Render

Guía completa para desplegar Smart Condominium en Render.

## 📋 Pasos para desplegar en Render

### 1. Preparar el repositorio
```bash
# Asegúrate de que todos los archivos estén en GitHub
git add .
git commit -m "Configuración para Render"
git push origin main
```

### 2. Crear base de datos PostgreSQL en Render

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "PostgreSQL"
3. Configuración:
   - **Name:** `condominiobd`
   - **Database:** `condominiobd`
   - **User:** `smart_condo_user`
   - **Region:** Oregon (US West)
   - **PostgreSQL Version:** 15
   - **Plan:** Free (para pruebas)

4. Click "Create Database"
5. **¡IMPORTANTE!** Copia la "External Database URL" - la necesitarás

### 3. Crear Web Service en Render

1. En Render Dashboard, click "New" → "Web Service"
2. Conecta tu repositorio GitHub
3. Configuración:
   - **Name:** `smart-condominium`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** (dejar vacío)
   - **Environment:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn smart_condominium.wsgi:application`

### 4. Configurar Variables de Entorno

En el Web Service, ve a "Environment" y agrega:

```
DATABASE_URL=postgresql://smart_condo_user:password@dpg-xxxxx-a.oregon-postgres.render.com/condominiobd
SECRET_KEY=tu-clave-secreta-super-segura-para-produccion
DJANGO_SETTINGS_MODULE=smart_condominium.settings.production
WEB_CONCURRENCY=4
```

**¡IMPORTANTE!** Reemplaza `DATABASE_URL` con la URL que copiaste del paso 2.

### 5. Deploy

1. Click "Create Web Service"
2. Render automáticamente:
   - Clonará tu repositorio
   - Ejecutará `build.sh`
   - Instalará dependencias
   - Ejecutará migraciones
   - Creará usuarios predeterminados
   - Iniciará la aplicación

### 6. Verificar despliegue

Una vez completado, tu aplicación estará disponible en:
- **URL:** `https://smart-condominium.onrender.com`
- **Admin:** `https://smart-condominium.onrender.com/admin/`
- **API:** `https://smart-condominium.onrender.com/api/`

## 🔐 Usuarios Predeterminados

Se crean automáticamente:

| Usuario | Contraseña | Email | Rol |
|---------|------------|-------|-----|
| `admin` | `admin123` | admin@smartcondo.com | Administrador |
| `demo.residente` | `demo123` | demo@smartcondo.com | Residente |
| `demo.seguridad` | `security123` | seguridad@smartcondo.com | Seguridad |

## 🔧 Comandos útiles para debugging

### Ver logs en tiempo real
1. Ve a tu Web Service en Render
2. Click en la pestaña "Logs"

### Ejecutar comandos en la aplicación
```bash
# No es posible SSH en Render Free, pero puedes:
# 1. Agregar comandos al build.sh
# 2. Crear endpoints de debugging
# 3. Usar logs para debugging
```

### Redeployar
```bash
git add .
git commit -m "Update"
git push origin main
# Render redeploy automáticamente
```

## 🛠️ Solución de problemas comunes

### Error: "Build failed"
- Revisa los logs en Render
- Verifica que `build.sh` sea ejecutable: `chmod +x build.sh`
- Asegúrate de que requirements.txt esté actualizado

### Error: "Database connection failed"
- Verifica que DATABASE_URL esté correcta
- Asegúrate de que la base de datos PostgreSQL esté creada
- Revisa que el usuario y contraseña sean correctos

### Error: "Static files not found"
- WhiteNoise debería manejar archivos estáticos automáticamente
- Verifica que `collectstatic` se ejecute en build.sh

### App muy lenta al iniciar
- Render Free tiene "cold starts" - es normal
- Considera upgrade a plan paid para mejor performance

## 💡 Tips para Render

1. **Free Plan Limitations:**
   - La app se "duerme" después de 15 min de inactividad
   - Tarda ~30 segundos en "despertar"
   - Considera ping service o upgrade a paid

2. **Database Free Plan:**
   - Expira después de 90 días
   - Haz backups regulares
   - Considera upgrade para producción

3. **Custom Domain:**
   - Solo disponible en planes paid
   - Se puede configurar en "Settings" → "Custom Domains"

## 🎉 ¡Listo!

Tu Smart Condominium está desplegado en Render con:
- ✅ PostgreSQL database
- ✅ Usuarios automáticos
- ✅ API REST completa
- ✅ Panel de administración
- ✅ SSL automático (HTTPS)
- ✅ Redeploy automático desde GitHub