"""
Script para ejecutar desde Render Console o Shell
Crea superusuarios y gestiona usuarios directamente en producción
"""

# Para ejecutar desde Render Console:
# 1. Ve a tu servicio en Render
# 2. Haz clic en "Console" o "Shell"
# 3. Ejecuta: python manage.py shell
# 4. Copia y pega este código

from django.contrib.auth import get_user_model
from apps.autenticacion.models import PerfilUsuario

User = get_user_model()

def crear_superusuario(email, password, nombre="", apellido=""):
    """Crear un nuevo superusuario"""
    
    # Verificar si ya existe
    if User.objects.filter(email=email).exists():
        print(f"❌ Usuario con email {email} ya existe")
        return None
    
    # Crear superusuario
    user = User.objects.create_superuser(
        username=email,
        email=email,
        password=password,
        first_name=nombre,
        last_name=apellido
    )
    
    # Crear perfil
    perfil, created = PerfilUsuario.objects.get_or_create(
        usuario=user,
        defaults={'rol': 'administrador'}
    )
    
    print(f"✅ Superusuario creado: {email}")
    print(f"👤 Nombre: {user.get_full_name()}")
    print(f"🔗 Admin: https://back-smart-condominium-1.onrender.com/admin/")
    
    return user

def listar_usuarios():
    """Listar todos los usuarios"""
    print("📋 USUARIOS EN EL SISTEMA:")
    print("-" * 50)
    
    users = User.objects.all()
    for user in users:
        status = "✅ Activo" if user.is_active else "❌ Inactivo"
        role = "👑 Super" if user.is_superuser else "👤 User"
        print(f"• {user.email} ({user.get_full_name()}) - {status} - {role}")
    
    print(f"\nTotal: {users.count()} usuarios")

def eliminar_usuario(email):
    """Eliminar un usuario"""
    try:
        user = User.objects.get(email=email)
        user.delete()
        print(f"✅ Usuario {email} eliminado")
    except User.DoesNotExist:
        print(f"❌ Usuario {email} no existe")

# 🚀 EJEMPLOS DE USO:

print("🔧 COMANDOS DISPONIBLES:")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("1. crear_superusuario('admin@ejemplo.com', 'password123', 'Admin', 'Sistema')")
print("2. listar_usuarios()")
print("3. eliminar_usuario('usuario@ejemplo.com')")
print("")
print("💡 EJEMPLO RÁPIDO:")
print("crear_superusuario('admin@condominio.com', 'Admin123!', 'Administrador', 'Sistema')")

# Para crear un superusuario inmediatamente, descomenta la siguiente línea:
# crear_superusuario('admin@condominio.com', 'Admin123!', 'Administrador', 'Sistema')