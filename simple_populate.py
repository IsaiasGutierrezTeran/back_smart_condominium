#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_condominium.settings.base')
django.setup()

from django.contrib.auth.models import Group
from apps.autenticacion.models import Usuario, PerfilUsuario
from apps.finanzas.models import UnidadHabitacional

def main():
    """Poblar base de datos rápidamente"""
    try:
        print("🚀 POBLANDO BASE DE DATOS CONDOMINIOBD")
        print("=" * 50)
        
        # Limpiar usuarios existentes
        print("🧹 Limpiando usuarios...")
        PerfilUsuario.objects.all().delete()
        Usuario.objects.all().delete()
        UnidadHabitacional.objects.all().delete()
        
        # Crear grupos
        print("👥 Creando grupos...")
        Group.objects.get_or_create(name='Administradores')
        Group.objects.get_or_create(name='Residentes')
        Group.objects.get_or_create(name='Seguridad')
        Group.objects.get_or_create(name='Mantenimiento')
        
        # Crear admin
        print("👤 Creando administrador...")
        admin = Usuario.objects.create_user(
            username='admin',
            email='admin@condo.com',
            first_name='Admin',
            last_name='Sistema',
            telefono='555-0001',
            is_staff=True,
            is_superuser=True
        )
        admin.groups.add(Group.objects.get(name='Administradores'))
        
        PerfilUsuario.objects.create(
            usuario=admin,
            rol='administrador',
            contacto_emergencia='Sistema +555-9001',
            es_propietario=False
        )
        
        # Crear 10 residentes
        print("🏠 Creando residentes...")
        residentes_data = [
            ('juan.perez', 'juan@email.com', 'Juan', 'Pérez', '555-0101', '101', 'A'),
            ('maria.garcia', 'maria@email.com', 'María', 'García', '555-0102', '102', 'A'),
            ('carlos.lopez', 'carlos@email.com', 'Carlos', 'López', '555-0201', '201', 'A'),
            ('ana.martinez', 'ana@email.com', 'Ana', 'Martínez', '555-0202', '202', 'A'),
            ('pedro.rodriguez', 'pedro@email.com', 'Pedro', 'Rodríguez', '555-0301', '301', 'A'),
            ('sofia.hernandez', 'sofia@email.com', 'Sofía', 'Hernández', '555-0302', '302', 'A'),
            ('luis.gonzalez', 'luis@email.com', 'Luis', 'González', '555-0401', '401', 'A'),
            ('carmen.ruiz', 'carmen@email.com', 'Carmen', 'Ruiz', '555-0402', '402', 'A'),
            ('miguel.torres', 'miguel@email.com', 'Miguel', 'Torres', '555-0501', '501', 'A'),
            ('elena.vargas', 'elena@email.com', 'Elena', 'Vargas', '555-0502', '502', 'A')
        ]
        
        usuarios_creados = []
        for username, email, first_name, last_name, telefono, unidad, edificio in residentes_data:
            user = Usuario.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                telefono=telefono
            )
            user.groups.add(Group.objects.get(name='Residentes'))
            
            PerfilUsuario.objects.create(
                usuario=user,
                rol='residente',
                numero_unidad=unidad,
                edificio=edificio,
                contacto_emergencia=f'Contacto {first_name} +555-9{unidad}',
                es_propietario=True
            )
            usuarios_creados.append(user)
            print(f"✅ Usuario creado: {username}")
        
        # Crear personal de seguridad
        print("🛡️ Creando personal de seguridad...")
        security1 = Usuario.objects.create_user(
            username='seguridad01',
            email='seguridad1@condo.com',
            first_name='Roberto',
            last_name='Seguridad',
            telefono='555-0701'
        )
        security1.groups.add(Group.objects.get(name='Seguridad'))
        
        PerfilUsuario.objects.create(
            usuario=security1,
            rol='seguridad',
            contacto_emergencia='Jefe Seguridad +555-9701',
            es_propietario=False
        )
        
        security2 = Usuario.objects.create_user(
            username='seguridad02',
            email='seguridad2@condo.com',
            first_name='Pedro',
            last_name='Vigilancia',
            telefono='555-0702'
        )
        security2.groups.add(Group.objects.get(name='Seguridad'))
        
        PerfilUsuario.objects.create(
            usuario=security2,
            rol='seguridad',
            contacto_emergencia='Jefe Seguridad +555-9702',
            es_propietario=False
        )
        
        # Crear personal de mantenimiento
        print("🔧 Creando personal de mantenimiento...")
        maintenance = Usuario.objects.create_user(
            username='mantenimiento01',
            email='mantenimiento@condo.com',
            first_name='Luis',
            last_name='Mantenimiento',
            telefono='555-0801'
        )
        maintenance.groups.add(Group.objects.get(name='Mantenimiento'))
        
        PerfilUsuario.objects.create(
            usuario=maintenance,
            rol='mantenimiento',
            contacto_emergencia='Supervisor +555-9801',
            es_propietario=False
        )
        
        # Crear unidades habitacionales
        print("🏢 Creando unidades habitacionales...")
        residentes = Usuario.objects.filter(groups__name='Residentes')
        
        for i, (username, email, first_name, last_name, telefono, unidad, edificio) in enumerate(residentes_data):
            propietario = residentes[i]
            
            UnidadHabitacional.objects.create(
                numero_unidad=unidad,
                edificio=edificio,
                propietario=propietario,
                area_m2=85.5 + (i * 5),  # Variando el área
                dormitorios=2 + (i % 2)  # 2 o 3 dormitorios
            )
            print(f"✅ Unidad creada: {edificio}-{unidad}")
        
        print("\n🎉 ¡BASE DE DATOS POBLADA EXITOSAMENTE!")
        print("=" * 50)
        print("📊 RESUMEN:")
        print(f"👥 Usuarios: {Usuario.objects.count()}")
        print(f"👤 Perfiles: {PerfilUsuario.objects.count()}")
        print(f"🏠 Unidades: {UnidadHabitacional.objects.count()}")
        print(f"🏢 Administradores: {Usuario.objects.filter(groups__name='Administradores').count()}")
        print(f"🏠 Residentes: {Usuario.objects.filter(groups__name='Residentes').count()}")
        print(f"🛡️ Seguridad: {Usuario.objects.filter(groups__name='Seguridad').count()}")
        print(f"🔧 Mantenimiento: {Usuario.objects.filter(groups__name='Mantenimiento').count()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()