#!/usr/bin/env python
"""
Script para cargar datos iniciales en la base de datos
Ejecutado automáticamente durante la construcción del contenedor Docker
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_condominium.settings.production')
django.setup()

from django.contrib.auth.models import Group
from apps.autenticacion.models import Usuario, PerfilUsuario

def create_initial_data():
    """Crear datos iniciales si no existen"""
    try:
        print("🚀 Cargando datos iniciales...")
        
        # Crear grupos si no existen
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        residents_group, created = Group.objects.get_or_create(name='Residentes')
        security_group, created = Group.objects.get_or_create(name='Seguridad')
        maintenance_group, created = Group.objects.get_or_create(name='Mantenimiento')
        
        # Crear superusuario predeterminado si no existe
        if not Usuario.objects.filter(username='admin').exists():
            print("👤 Creando usuario administrador predeterminado...")
            
            admin_user = Usuario.objects.create_superuser(
                username='admin',
                email='admin@smartcondo.com',
                password='admin123',  # Contraseña predeterminada
                first_name='Administrator',
                last_name='System',
                telefono='555-0001'
            )
            
            # Agregar al grupo de administradores
            admin_user.groups.add(admin_group)
            
            # Crear perfil para el administrador
            PerfilUsuario.objects.create(
                usuario=admin_user,
                rol='administrador',
                contacto_emergencia='Sistema Administrativo +555-9001',
                es_propietario=False
            )
            
            print("✅ Usuario administrador creado exitosamente")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: admin@smartcondo.com")
        else:
            print("ℹ️  Usuario administrador ya existe")
        
        # Crear usuario demo residente si no existe
        if not Usuario.objects.filter(username='demo.residente').exists():
            print("🏠 Creando usuario demo residente...")
            
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
                contacto_emergencia='Contacto Demo +555-9100',
                es_propietario=True
            )
            
            print("✅ Usuario demo residente creado exitosamente")
            print("   Username: demo.residente")
            print("   Password: demo123")
        else:
            print("ℹ️  Usuario demo ya existe")
        
        # Crear usuario de seguridad demo si no existe
        if not Usuario.objects.filter(username='demo.seguridad').exists():
            print("🛡️ Creando usuario demo seguridad...")
            
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
            
            print("✅ Usuario demo seguridad creado exitosamente")
            print("   Username: demo.seguridad")
            print("   Password: security123")
        else:
            print("ℹ️  Usuario seguridad demo ya existe")
        
        print("\n🎉 Datos iniciales cargados correctamente!")
        
        # Mostrar resumen
        total_users = Usuario.objects.count()
        total_profiles = PerfilUsuario.objects.count()
        
        print(f"📊 Resumen:")
        print(f"   👥 Total usuarios: {total_users}")
        print(f"   👤 Total perfiles: {total_profiles}")
        print(f"   🏢 Administradores: {Usuario.objects.filter(groups__name='Administradores').count()}")
        print(f"   🏠 Residentes: {Usuario.objects.filter(groups__name='Residentes').count()}")
        print(f"   🛡️ Seguridad: {Usuario.objects.filter(groups__name='Seguridad').count()}")
        
    except Exception as e:
        print(f"❌ Error cargando datos iniciales: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    create_initial_data()