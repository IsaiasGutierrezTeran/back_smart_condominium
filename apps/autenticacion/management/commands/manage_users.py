"""
Comando personalizado para crear superusuario desde Render
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.autenticacion.models import PerfilUsuario

User = get_user_model()

class Command(BaseCommand):
    help = 'Crear superusuario y gestionar usuarios desde Render'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email del usuario')
        parser.add_argument('--password', type=str, help='Password del usuario')
        parser.add_argument('--first-name', type=str, help='Nombre del usuario')
        parser.add_argument('--last-name', type=str, help='Apellido del usuario')
        parser.add_argument('--action', type=str, choices=['create', 'list', 'delete'], 
                          default='create', help='Acción a realizar')

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'list':
            self.list_users()
        elif action == 'create':
            self.create_user(options)
        elif action == 'delete':
            self.delete_user(options)

    def list_users(self):
        """Listar todos los usuarios"""
        self.stdout.write("📋 USUARIOS EN EL SISTEMA:")
        self.stdout.write("-" * 50)
        
        users = User.objects.all()
        for user in users:
            status = "✅ Activo" if user.is_active else "❌ Inactivo"
            role = "👑 Superusuario" if user.is_superuser else "👤 Usuario"
            
            self.stdout.write(f"• {user.email} ({user.get_full_name()}) - {status} - {role}")
        
        self.stdout.write(f"\nTotal: {users.count()} usuarios")

    def create_user(self, options):
        """Crear nuevo superusuario"""
        email = options.get('email')
        password = options.get('password')
        first_name = options.get('first_name', '')
        last_name = options.get('last_name', '')

        if not email or not password:
            self.stdout.write(
                self.style.ERROR("❌ Email y password son requeridos")
            )
            self.stdout.write("Ejemplo: python manage.py manage_users --email admin@ejemplo.com --password mipassword123")
            return

        # Verificar si el usuario ya existe
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f"❌ Usuario con email {email} ya existe")
            )
            return

        # Crear superusuario
        user = User.objects.create_superuser(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Crear perfil
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=user,
            defaults={'rol': 'administrador'}
        )

        self.stdout.write(
            self.style.SUCCESS(f"✅ Superusuario creado exitosamente: {email}")
        )
        self.stdout.write(f"👤 Nombre: {user.get_full_name()}")
        self.stdout.write(f"🔐 Password: {password}")
        self.stdout.write(f"🔗 Puede acceder en: https://back-smart-condominium-1.onrender.com/admin/")

    def delete_user(self, options):
        """Eliminar usuario"""
        email = options.get('email')
        
        if not email:
            self.stdout.write(
                self.style.ERROR("❌ Email es requerido para eliminar")
            )
            return

        try:
            user = User.objects.get(email=email)
            user.delete()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Usuario {email} eliminado exitosamente")
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"❌ Usuario con email {email} no existe")
            )