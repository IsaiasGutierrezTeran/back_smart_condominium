from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.autenticacion.models import Usuario, PerfilUsuario

class Command(BaseCommand):
    help = 'Crea usuarios predeterminados para el sistema'

    def handle(self, *args, **options):
        """Crear usuarios predeterminados"""
        self.stdout.write(self.style.SUCCESS('🚀 Creando usuarios predeterminados...'))
        
        try:
            # Crear grupos si no existen
            admin_group, _ = Group.objects.get_or_create(name='Administradores')
            residents_group, _ = Group.objects.get_or_create(name='Residentes')
            security_group, _ = Group.objects.get_or_create(name='Seguridad')
            maintenance_group, _ = Group.objects.get_or_create(name='Mantenimiento')
            
            # Crear superusuario administrador
            if not Usuario.objects.filter(username='admin').exists():
                admin_user = Usuario.objects.create_superuser(
                    username='admin',
                    email='admin@smartcondo.com',
                    password='admin123',
                    first_name='Administrator',
                    last_name='System',
                    telefono='555-0001'
                )
                admin_user.groups.add(admin_group)
                
                PerfilUsuario.objects.create(
                    usuario=admin_user,
                    rol='administrador',
                    contacto_emergencia='Sistema +555-9001',
                    es_propietario=False
                )
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Usuario administrador creado')
                )
                self.stdout.write('   Username: admin')
                self.stdout.write('   Password: admin123')
            else:
                self.stdout.write(
                    self.style.WARNING('ℹ️  Usuario admin ya existe')
                )
            
            # Crear usuario demo residente
            if not Usuario.objects.filter(username='demo.residente').exists():
                demo_user = Usuario.objects.create_user(
                    username='demo.residente',
                    email='demo@smartcondo.com',  
                    password='demo123',
                    first_name='Demo',
                    last_name='Residente',
                    telefono='555-0100'
                )
                demo_user.groups.add(residents_group)
                
                PerfilUsuario.objects.create(
                    usuario=demo_user,
                    rol='residente',
                    numero_unidad='101',
                    edificio='A',
                    contacto_emergencia='Demo Contact +555-9100',
                    es_propietario=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Usuario demo residente creado')
                )
                self.stdout.write('   Username: demo.residente')
                self.stdout.write('   Password: demo123')
            else:
                self.stdout.write(
                    self.style.WARNING('ℹ️  Usuario demo.residente ya existe')
                )
            
            # Crear usuario demo seguridad
            if not Usuario.objects.filter(username='demo.seguridad').exists():
                security_user = Usuario.objects.create_user(
                    username='demo.seguridad',
                    email='seguridad@smartcondo.com',
                    password='security123',
                    first_name='Demo',
                    last_name='Seguridad',
                    telefono='555-0200'
                )
                security_user.groups.add(security_group)
                
                PerfilUsuario.objects.create(
                    usuario=security_user,
                    rol='seguridad',
                    contacto_emergencia='Jefe Seguridad +555-9200',
                    es_propietario=False
                )
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Usuario demo seguridad creado')
                )
                self.stdout.write('   Username: demo.seguridad')
                self.stdout.write('   Password: security123')
            else:
                self.stdout.write(
                    self.style.WARNING('ℹ️  Usuario demo.seguridad ya existe')
                )
            
            # Mostrar resumen
            total_users = Usuario.objects.count()
            self.stdout.write(
                self.style.SUCCESS(f'\n🎉 Proceso completado! Total usuarios: {total_users}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creando usuarios: {e}')
            )
            raise