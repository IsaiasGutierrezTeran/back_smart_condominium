#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_condominium.settings.base')
django.setup()

from django.contrib.auth.models import Group
from apps.autenticacion.models import Usuario, PerfilUsuario
from apps.finanzas.models import UnidadHabitacional, TipoPago, Pago, Multa
from apps.comunicacion.models import AvisoGeneral, CategoriaNotificacion, Notificacion
from apps.reservas.models import ReservaEspacio, EspacioComun, TipoEspacio
from apps.seguridad.models import IncidenteSeguridad, TipoIncidente, VehiculoAutorizado, RegistroVisita

def clear_data():
    """Limpiar datos existentes"""
    print("🧹 Limpiando datos existentes...")
    
    # Limpiar en orden inverso a las dependencias
    RegistroVisita.objects.all().delete()
    VehiculoAutorizado.objects.all().delete()
    Incidente.objects.all().delete()
    Reserva.objects.all().delete()
    Pago.objects.all().delete()
    Multa.objects.all().delete()
    Comunicado.objects.all().delete()
    PerfilUsuario.objects.all().delete()
    Usuario.objects.all().delete()
    UnidadHabitacional.objects.all().delete()
    EspacioComun.objects.all().delete()
    TipoEspacio.objects.all().delete()
    TipoPago.objects.all().delete()
    TipoComunicado.objects.all().delete()
    TipoIncidente.objects.all().delete()
    
    print("✅ Datos limpiados")

def create_groups():
    """Crear grupos de usuarios"""
    groups = ['Administradores', 'Residentes', 'Seguridad', 'Mantenimiento']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
    print("✅ Grupos creados")

def create_users():
    """Crear usuarios básicos"""
    print("👥 Creando usuarios...")
    
    # Crear admin
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
    
    # Crear residentes
    residentes_data = [
        ('juan.perez', 'juan@email.com', 'Juan', 'Pérez', '555-0101', '101', 'A'),
        ('maria.garcia', 'maria@email.com', 'María', 'García', '555-0102', '102', 'A'),
        ('carlos.lopez', 'carlos@email.com', 'Carlos', 'López', '555-0201', '201', 'A'),
        ('ana.martinez', 'ana@email.com', 'Ana', 'Martínez', '555-0202', '202', 'A'),
        ('pedro.rodriguez', 'pedro@email.com', 'Pedro', 'Rodríguez', '555-0301', '301', 'A'),
        ('sofia.hernandez', 'sofia@email.com', 'Sofía', 'Hernández', '555-0302', '302', 'A'),
        ('luis.gonzalez', 'luis@email.com', 'Luis', 'González', '555-0101', '101', 'B'),
        ('carmen.ruiz', 'carmen@email.com', 'Carmen', 'Ruiz', '555-0102', '102', 'B'),
        ('miguel.torres', 'miguel@email.com', 'Miguel', 'Torres', '555-0201', '201', 'B'),
        ('elena.vargas', 'elena@email.com', 'Elena', 'Vargas', '555-0202', '202', 'B')
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
    
    # Crear personal de seguridad
    security = Usuario.objects.create_user(
        username='seguridad01',
        email='seguridad@condo.com',
        first_name='Roberto',
        last_name='Seguridad',
        telefono='555-0401'
    )
    security.groups.add(Group.objects.get(name='Seguridad'))
    
    PerfilUsuario.objects.create(
        usuario=security,
        rol='seguridad',
        contacto_emergencia='Jefe Seguridad +555-9401',
        es_propietario=False
    )
    
    print(f"✅ {len(usuarios_creados) + 2} usuarios creados")
    return usuarios_creados

def create_units():
    """Crear unidades habitacionales"""
    print("🏠 Creando unidades...")
    
    residentes = Usuario.objects.filter(groups__name='Residentes')
    
    unidades_data = [
        ('101', 'A', 85.5, 2),
        ('102', 'A', 92.0, 3),
        ('201', 'A', 85.5, 2),
        ('202', 'A', 92.0, 3),
        ('301', 'A', 85.5, 2),
        ('302', 'A', 92.0, 3),
        ('101', 'B', 110.0, 3),
        ('102', 'B', 110.0, 3),
        ('201', 'B', 110.0, 3),
        ('202', 'B', 110.0, 3)
    ]
    
    for i, (numero, edificio, area, dormitorios) in enumerate(unidades_data):
        propietario = residentes[i] if i < len(residentes) else residentes[0]
        
        UnidadHabitacional.objects.create(
            numero_unidad=numero,
            edificio=edificio,
            propietario=propietario,
            area_m2=area,
            dormitorios=dormitorios
        )
    
    print("✅ 10 unidades creadas")

def create_basic_data():
    """Crear datos básicos del sistema"""
    print("📊 Creando datos básicos...")
    
    # Tipos de pago
    tipos_pago = ['Administración', 'Multa', 'Cuota Extraordinaria', 'Servicios']
    for tipo in tipos_pago:
        TipoPago.objects.get_or_create(nombre=tipo)
    
    # Tipos de comunicado
    tipos_comunicado = ['Informativo', 'Urgente', 'Mantenimiento', 'Evento']
    for tipo in tipos_comunicado:
        TipoComunicado.objects.get_or_create(nombre=tipo)
    
    # Tipos de incidente
    tipos_incidente = ['Seguridad', 'Ruido', 'Daños', 'Otros']
    for tipo in tipos_incidente:
        TipoIncidente.objects.get_or_create(nombre=tipo)
    
    # Tipos de espacio
    tipos_espacio = ['Salón Social', 'Gimnasio', 'Piscina', 'Cancha']
    for tipo in tipos_espacio:
        TipoEspacio.objects.get_or_create(nombre=tipo)
    
    print("✅ Tipos básicos creados")

def create_sample_records():
    """Crear registros de ejemplo"""
    print("📝 Creando registros de ejemplo...")
    
    # Comunicados
    admin = Usuario.objects.filter(is_superuser=True).first()
    tipo_info = TipoComunicado.objects.get(nombre='Informativo')
    
    for i in range(5):
        Comunicado.objects.create(
            titulo=f'Comunicado {i+1}',
            contenido=f'Contenido del comunicado número {i+1}',
            tipo=tipo_info,
            autor=admin,
            dirigido_a='todos'
        )
    
    # Espacios comunes
    tipo_salon = TipoEspacio.objects.get(nombre='Salón Social')
    tipo_gym = TipoEspacio.objects.get(nombre='Gimnasio')
    
    EspacioComun.objects.create(
        nombre='Salón Principal',
        tipo=tipo_salon,
        capacidad_maxima=50,
        costo_reserva=Decimal('100.00')
    )
    
    EspacioComun.objects.create(
        nombre='Gimnasio',
        tipo=tipo_gym,
        capacidad_maxima=20,
        costo_reserva=Decimal('50.00')
    )
    
    # Reservas
    residente = Usuario.objects.filter(groups__name='Residentes').first()
    salon = EspacioComun.objects.first()
    
    for i in range(3):
        fecha_inicio = datetime.now() + timedelta(days=i+1)
        Reserva.objects.create(
            residente=residente,
            espacio=salon,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_inicio + timedelta(hours=4),
            costo_total=salon.costo_reserva,
            estado='confirmada'
        )
    
    print("✅ Registros de ejemplo creados")

def main():
    """Función principal"""
    try:
        print("🚀 POBLANDO BASE DE DATOS CONDOMINIOBD")
        print("=" * 50)
        
        clear_data()
        create_groups()
        create_users()
        create_units()
        create_basic_data()
        create_sample_records()
        
        print("\n🎉 ¡BASE DE DATOS POBLADA EXITOSAMENTE!")
        print("=" * 50)
        print("📊 RESUMEN:")
        print(f"👥 Usuarios: {Usuario.objects.count()}")
        print(f"🏠 Unidades: {UnidadHabitacional.objects.count()}")
        print(f"📢 Comunicados: {Comunicado.objects.count()}")
        print(f"🏢 Espacios: {EspacioComun.objects.count()}")
        print(f"📅 Reservas: {Reserva.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()