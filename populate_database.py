#!/usr/bin/env python
"""
Script para poblar la base de datos del Smart Condominium con datos de ejemplo
"""
import os
import sys
import django
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_condominium.settings.base')

# Setup Django
django.setup()

from django.contrib.auth.models import Group, Permission
from apps.autenticacion.models import Usuario, PerfilUsuario
from apps.finanzas.models import (
    UnidadHabitacional, TipoPago, Pago, Multa, 
    HistorialPago
)
from apps.comunicacion.models import (
    CategoriaNotificacion, AvisoGeneral, Notificacion,
    PlantillaNotificacion
)
from apps.reservas.models import (
    TipoAreaComun, AreaComun, ServicioAdicional,
    Reserva, ReservaServicio
)
from apps.seguridad.models import (
    TipoVisitante, RegistroVisitante, AccesoVehiculo,
    RegistroAcceso, IncidenteSeguridad, ConfiguracionIA,
    AnalisisPredictivoMorosidad
)

def create_usuarios_and_perfiles():
    """Crear usuarios con diferentes roles"""
    print("🧑‍💼 Creando usuarios y perfiles...")
    
    # Crear grupos si no existen
    admin_group, _ = Group.objects.get_or_create(name='Administradores')
    residents_group, _ = Group.objects.get_or_create(name='Residentes')
    security_group, _ = Group.objects.get_or_create(name='Seguridad')
    maintenance_group, _ = Group.objects.get_or_create(name='Mantenimiento')
    
    usuarios_data = [
        {
            'username': 'admin',
            'email': 'admin@smartcondo.com',
            'first_name': 'Administrator',
            'last_name': 'System',
            'telefono': '+1-555-0001',
            'is_staff': True,
            'is_superuser': True,
            'grupo': admin_group,
            'perfil_data': {
                'rol': 'administrador',
                'contacto_emergencia': 'Administración General',
                'es_propietario': False
            }
        },
        {
            'username': 'juan.perez',
            'email': 'juan.perez@email.com',
            'first_name': 'Juan Carlos',
            'last_name': 'Pérez González',
            'telefono': '+1-555-0101',
            'grupo': residents_group,
            'perfil_data': {
                'rol': 'residente',
                'numero_unidad': '101',
                'edificio': 'A',
                'contacto_emergencia': 'María Pérez +1-555-9101',
                'es_propietario': True
            }
        },
        {
            'username': 'maria.garcia',
            'email': 'maria.garcia@email.com',
            'first_name': 'María José',
            'last_name': 'García Rodríguez',
            'telefono': '+1-555-0102',
            'grupo': residents_group,
            'perfil_data': {
                'rol': 'residente',
                'numero_unidad': '102',
                'edificio': 'A',
                'contacto_emergencia': 'Carlos García +1-555-9102',
                'es_propietario': True
            }
        },
        {
            'username': 'carlos.martinez',
            'email': 'carlos.martinez@email.com',
            'first_name': 'Carlos Alberto',
            'last_name': 'Martínez López',
            'telefono': '+1-555-0201',
            'grupo': residents_group,
            'perfil_data': {
                'rol': 'residente',
                'numero_unidad': '201',
                'edificio': 'A',
                'contacto_emergencia': 'Elena Martínez +1-555-9201',
                'es_propietario': True
            }
        },
        {
            'username': 'ana.lopez',
            'email': 'ana.lopez@email.com',
            'first_name': 'Ana Patricia',
            'last_name': 'López Herrera',
            'telefono': '+1-555-0202',
            'grupo': residents_group,
            'perfil_data': {
                'rol': 'residente',
                'numero_unidad': '202',
                'edificio': 'A',
                'contacto_emergencia': 'Pedro López +1-555-9202',
                'es_propietario': False
            }
        },
        {
            'username': 'security.chief',
            'email': 'seguridad@smartcondo.com',
            'first_name': 'Roberto',
            'last_name': 'Vargas Sánchez',
            'telefono': '+1-555-0301',
            'grupo': security_group,
            'perfil_data': {
                'rol': 'seguridad',
                'contacto_emergencia': 'Carmen Vargas +1-555-9301',
                'es_propietario': False
            }
        },
        {
            'username': 'security.guard1',
            'email': 'guardia1@smartcondo.com',
            'first_name': 'Pedro',
            'last_name': 'Ramírez Torres',
            'telefono': '+1-555-0302',
            'grupo': security_group,
            'perfil_data': {
                'rol': 'seguridad',
                'contacto_emergencia': 'Ana Ramírez +1-555-9302',
                'es_propietario': False
            }
        },
        {
            'username': 'maintenance.chief',
            'email': 'mantenimiento@smartcondo.com',
            'first_name': 'Luis Fernando',
            'last_name': 'Morales Castro',
            'telefono': '+1-555-0401',
            'grupo': maintenance_group,
            'perfil_data': {
                'rol': 'mantenimiento',
                'contacto_emergencia': 'Rosa Morales +1-555-9401',
                'es_propietario': False
            }
        },
        {
            'username': 'sofia.rivera',
            'email': 'sofia.rivera@email.com',
            'first_name': 'Sofía Elena',
            'last_name': 'Rivera Mendoza',
            'telefono': '+1-555-0301',
            'grupo': residents_group,
            'perfil_data': {
                'rol': 'residente',
                'numero_unidad': '301',
                'edificio': 'A',
                'contacto_emergencia': 'Mario Rivera +1-555-9301',
                'es_propietario': True
            }
        },
        {
            'username': 'miguel.torres',
            'email': 'miguel.torres@email.com',
            'first_name': 'Miguel Ángel',
            'last_name': 'Torres Jiménez',
            'telefono': '+1-555-0302',
            'grupo': residents_group,
            'perfil_data': {
                'rol': 'residente',
                'numero_unidad': '302',
                'edificio': 'A',
                'contacto_emergencia': 'Lucia Torres +1-555-9302',
                'es_propietario': True
            }
        }
    ]
    
    usuarios_creados = []
    for user_data in usuarios_data:
        perfil_data = user_data.pop('perfil_data')
        grupo = user_data.pop('grupo')
        
        # Crear usuario
        usuario, created = Usuario.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        
        if created:
            usuario.set_password('password123')  # Contraseña por defecto
            usuario.save()
            usuario.groups.add(grupo)
            
            # Crear perfil
            PerfilUsuario.objects.get_or_create(
                usuario=usuario,
                defaults=perfil_data
            )
            
            usuarios_creados.append(usuario)
            print(f"✅ Usuario creado: {usuario.username} - {usuario.get_full_name()}")
    
    print(f"📊 Total usuarios creados: {len(usuarios_creados)}")
    return usuarios_creados

def create_unidades_habitacionales():
    """Crear unidades habitacionales"""
    print("\n🏠 Creando unidades habitacionales...")
    
    unidades_data = [
        {'numero_unidad': '101', 'edificio': 'A', 'area_m2': 85.5, 'dormitorios': 2},
        {'numero_unidad': '102', 'edificio': 'A', 'area_m2': 92.0, 'dormitorios': 3},
        {'numero_unidad': '201', 'edificio': 'A', 'area_m2': 85.5, 'dormitorios': 2},
        {'numero_unidad': '202', 'edificio': 'A', 'area_m2': 92.0, 'dormitorios': 3},
        {'numero_unidad': '301', 'edificio': 'A', 'area_m2': 85.5, 'dormitorios': 2},
        {'numero_unidad': '302', 'edificio': 'A', 'area_m2': 92.0, 'dormitorios': 3},
        {'numero_unidad': '101', 'edificio': 'B', 'area_m2': 110.0, 'dormitorios': 3},
        {'numero_unidad': '102', 'edificio': 'B', 'area_m2': 110.0, 'dormitorios': 3},
        {'numero_unidad': '201', 'edificio': 'B', 'area_m2': 110.0, 'dormitorios': 3},
        {'numero_unidad': '202', 'edificio': 'B', 'area_m2': 110.0, 'dormitorios': 3}
    ]
    
    # Asignar propietarios a las unidades
    residentes = Usuario.objects.filter(groups__name='Residentes')[:len(unidades_data)]
    
    unidades_creadas = []
    for i, unidad_data in enumerate(unidades_data):
        if i < len(residentes):
            unidad_data['propietario'] = residentes[i]
        
        unidad, created = UnidadHabitacional.objects.get_or_create(
            numero_unidad=unidad_data['numero_unidad'],
            edificio=unidad_data['edificio'],
            defaults=unidad_data
        )
        
        if created:
            unidades_creadas.append(unidad)
            print(f"✅ Unidad creada: {unidad.edificio}-{unidad.numero_unidad}")
    
    print(f"📊 Total unidades creadas: {len(unidades_creadas)}")
    return unidades_creadas

def create_finanzas_data():
    """Crear datos de finanzas"""
    print("\n💰 Creando datos financieros...")
    
    # Crear tipos de pago
    tipos_pago_data = [
        {'nombre': 'Administración', 'descripcion': 'Cuota mensual de administración', 'es_recurrente': True},
        {'nombre': 'Multa Parqueadero', 'descripcion': 'Multa por mal uso del parqueadero', 'es_recurrente': False},
        {'nombre': 'Cuota Extraordinaria', 'descripcion': 'Cuota especial para proyectos', 'es_recurrente': False},
        {'nombre': 'Servicios Públicos', 'descripcion': 'Agua, luz, gas común', 'es_recurrente': True},
        {'nombre': 'Seguridad', 'descripcion': 'Cuota de seguridad privada', 'es_recurrente': True},
        {'nombre': 'Mantenimiento', 'descripcion': 'Fondos para mantenimiento', 'es_recurrente': True},
        {'nombre': 'Fondo de Reserva', 'descripcion': 'Ahorro para emergencias', 'es_recurrente': True},
        {'nombre': 'Multa Ruido', 'descripcion': 'Multa por alteración del orden', 'es_recurrente': False},
        {'nombre': 'Uso de Salón', 'descripcion': 'Alquiler del salón comunal', 'es_recurrente': False},
        {'nombre': 'Parqueadero Visitante', 'descripcion': 'Uso del parqueadero para visitantes', 'es_recurrente': False}
    ]
    
    tipos_creados = []
    for tipo_data in tipos_pago_data:
        tipo, created = TipoPago.objects.get_or_create(
            nombre=tipo_data['nombre'],
            defaults=tipo_data
        )
        if created:
            tipos_creados.append(tipo)
    
    # Crear pagos
    unidades = list(UnidadHabitacional.objects.all())
    tipos_pago = list(TipoPago.objects.all())
    admin_user = Usuario.objects.filter(is_staff=True).first()
    
    pagos_creados = []
    for i in range(15):  # Crear 15 pagos
        unidad = random.choice(unidades)
        tipo_pago = random.choice(tipos_pago)
        
        # Generar fechas aleatorias en los últimos 6 meses
        fecha_base = timezone.now() - timedelta(days=180)
        fecha_vencimiento = fecha_base + timedelta(days=random.randint(0, 180))
        
        monto = Decimal(str(random.randint(50000, 500000)))
        
        pago_data = {
            'unidad': unidad,
            'tipo_pago': tipo_pago,
            'monto': monto,
            'fecha_vencimiento': fecha_vencimiento,
            'estado': random.choice(['pendiente', 'pagado', 'vencido']),
            'creado_por': admin_user
        }
        
        # Si está pagado, agregar fecha de pago
        if pago_data['estado'] == 'pagado':
            pago_data['fecha_pago'] = fecha_vencimiento - timedelta(days=random.randint(1, 30))
            pago_data['metodo_pago'] = random.choice(['efectivo', 'transferencia', 'tarjeta'])
        
        pago = Pago.objects.create(**pago_data)
        pagos_creados.append(pago)
    
    # Crear algunas multas
    multas_creadas = []
    for i in range(8):
        unidad = random.choice(unidades)
        
        multa_data = {
            'unidad': unidad,
            'concepto': random.choice([
                'Ruido excesivo después de las 10 PM',
                'Mal uso del parqueadero',
                'Mascotas sin correa en áreas comunes',
                'Daño a propiedad común',
                'Incumplimiento de normas de convivencia'
            ]),
            'monto': Decimal(str(random.randint(50000, 200000))),
            'fecha_imposicion': timezone.now() - timedelta(days=random.randint(1, 90)),
            'estado': random.choice(['activa', 'pagada', 'anulada']),
            'impuesta_por': admin_user
        }
        
        multa = Multa.objects.create(**multa_data)
        multas_creadas.append(multa)
    
    print(f"📊 Tipos de pago: {len(tipos_creados)}")
    print(f"📊 Pagos creados: {len(pagos_creados)}")
    print(f"📊 Multas creadas: {len(multas_creadas)}")

def create_comunicacion_data():
    """Crear datos de comunicación"""
    print("\n📢 Creando datos de comunicación...")
    
    # Crear categorías de notificación
    categorias_data = [
        {'nombre': 'Administración', 'descripcion': 'Avisos administrativos', 'color': '#007bff'},
        {'nombre': 'Mantenimiento', 'descripcion': 'Avisos de mantenimiento', 'color': '#ffc107'},
        {'nombre': 'Seguridad', 'descripcion': 'Avisos de seguridad', 'color': '#dc3545'},
        {'nombre': 'Eventos', 'descripcion': 'Eventos del condominio', 'color': '#28a745'},
        {'nombre': 'Emergencia', 'descripcion': 'Avisos de emergencia', 'color': '#dc3545'},
        {'nombre': 'Servicios', 'descripcion': 'Información de servicios', 'color': '#17a2b8'},
        {'nombre': 'Normas', 'descripcion': 'Recordatorios de normas', 'color': '#6c757d'},
        {'nombre': 'Celebraciones', 'descripcion': 'Fechas especiales', 'color': '#e83e8c'},
        {'nombre': 'Mejoras', 'descripcion': 'Proyectos de mejora', 'color': '#20c997'},
        {'nombre': 'Finanzas', 'descripcion': 'Avisos financieros', 'color': '#fd7e14'}
    ]
    
    categorias_creadas = []
    for cat_data in categorias_data:
        categoria, created = CategoriaNotificacion.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults=cat_data
        )
        if created:
            categorias_creadas.append(categoria)
    
    # Crear avisos generales
    admin_user = Usuario.objects.filter(is_staff=True).first()
    categorias = list(CategoriaNotificacion.objects.all())
    
    avisos_data = [
        {
            'titulo': 'Corte de agua programado',
            'contenido': 'Se informa que el próximo sábado de 8:00 AM a 2:00 PM habrá corte de agua por mantenimiento de tanques.',
            'categoria': 'Mantenimiento',
            'es_urgente': True
        },
        {
            'titulo': 'Nueva normativa de mascotas',
            'contenido': 'A partir del 1 de octubre, todas las mascotas deben estar registradas y usar correa en áreas comunes.',
            'categoria': 'Normas',
            'es_urgente': False
        },
        {
            'titulo': 'Asamblea General Extraordinaria',
            'contenido': 'Se convoca a asamblea para el 15 de octubre a las 7:00 PM en el salón comunal. Tema: Aprobación de cuota extraordinaria.',
            'categoria': 'Administración',
            'es_urgente': True
        },
        {
            'titulo': 'Mantenimiento de ascensores',
            'contenido': 'Los ascensores de la Torre B estarán fuera de servicio del 5 al 7 de octubre por mantenimiento preventivo.',
            'categoria': 'Mantenimiento',
            'es_urgente': False
        },
        {
            'titulo': 'Celebración del Día del Niño',
            'contenido': 'Los invitamos a la celebración del Día del Niño el sábado 12 de octubre en el área de juegos.',
            'categoria': 'Eventos',
            'es_urgente': False
        },
        {
            'titulo': 'Nuevo sistema de seguridad',
            'contenido': 'Se ha instalado un nuevo sistema de cámaras de seguridad con reconocimiento facial en el lobby principal.',
            'categoria': 'Seguridad',
            'es_urgente': False
        },
        {
            'titulo': 'Recordatorio: Pagos de administración',
            'contenido': 'Recordamos que los pagos de administración vencen el día 10 de cada mes. Evite recargos.',
            'categoria': 'Finanzas',
            'es_urgente': False
        },
        {
            'titulo': 'Mejoras en el gimnasio',
            'contenido': 'Se han adquirido nuevos equipos para el gimnasio. Estarán disponibles a partir del lunes.',
            'categoria': 'Mejoras',
            'es_urgente': False
        },
        {
            'titulo': 'Horarios de la piscina',
            'contenido': 'Los horarios de la piscina son: Lunes a viernes 6:00 AM - 10:00 PM, Sábados y domingos 7:00 AM - 9:00 PM.',
            'categoria': 'Servicios',
            'es_urgente': False
        },
        {
            'titulo': 'Simulacro de evacuación',
            'contenido': 'El próximo viernes se realizará un simulacro de evacuación a las 10:00 AM. Su participación es obligatoria.',
            'categoria': 'Emergencia',
            'es_urgente': True
        }
    ]
    
    avisos_creados = []
    for aviso_data in avisos_data:
        categoria_nombre = aviso_data.pop('categoria')
        categoria = next((c for c in categorias if c.nombre == categoria_nombre), categorias[0])
        
        aviso = AvisoGeneral.objects.create(
            titulo=aviso_data['titulo'],
            contenido=aviso_data['contenido'],
            categoria=categoria,
            es_urgente=aviso_data['es_urgente'],
            creado_por=admin_user,
            fecha_publicacion=timezone.now() - timedelta(days=random.randint(0, 30))
        )
        avisos_creados.append(aviso)
    
    print(f"📊 Categorías creadas: {len(categorias_creadas)}")
    print(f"📊 Avisos creados: {len(avisos_creados)}")

def create_reservas_data():
    """Crear datos de reservas"""
    print("\n🏊‍♂️ Creando datos de reservas...")
    
    # Crear tipos de áreas comunes
    tipos_areas_data = [
        {'nombre': 'Salón de Eventos', 'descripcion': 'Salón para celebraciones', 'requiere_deposito': True},
        {'nombre': 'Área Recreativa', 'descripcion': 'Zonas de esparcimiento', 'requiere_deposito': False},
        {'nombre': 'Deportivo', 'descripcion': 'Instalaciones deportivas', 'requiere_deposito': False},
        {'nombre': 'Piscina', 'descripcion': 'Áreas acuáticas', 'requiere_deposito': False},
        {'nombre': 'BBQ', 'descripcion': 'Zonas de asado', 'requiere_deposito': True},
        {'nombre': 'Estudio', 'descripcion': 'Salas de estudio', 'requiere_deposito': False},
        {'nombre': 'Gimnasio', 'descripcion': 'Equipos de ejercicio', 'requiere_deposito': False},
        {'nombre': 'Juegos Infantiles', 'descripcion': 'Área para niños', 'requiere_deposito': False},
        {'nombre': 'Terraza', 'descripcion': 'Espacios al aire libre', 'requiere_deposito': True},
        {'nombre': 'Sala de Juntas', 'descripcion': 'Reuniones formales', 'requiere_deposito': False}
    ]
    
    tipos_creados = []
    for tipo_data in tipos_areas_data:
        tipo, created = TipoAreaComun.objects.get_or_create(
            nombre=tipo_data['nombre'],
            defaults=tipo_data
        )
        if created:
            tipos_creados.append(tipo)
    
    # Crear áreas comunes
    tipos_areas = list(TipoAreaComun.objects.all())
    admin_user = Usuario.objects.filter(is_staff=True).first()
    
    areas_data = [
        {'nombre': 'Salón Comunal Principal', 'tipo': 'Salón de Eventos', 'capacidad_maxima': 80, 'costo_hora': Decimal('50000')},
        {'nombre': 'Piscina Adultos', 'tipo': 'Piscina', 'capacidad_maxima': 25, 'costo_hora': Decimal('0')},
        {'nombre': 'Piscina Niños', 'tipo': 'Piscina', 'capacidad_maxima': 15, 'costo_hora': Decimal('0')},
        {'nombre': 'Cancha de Tenis', 'tipo': 'Deportivo', 'capacidad_maxima': 4, 'costo_hora': Decimal('20000')},
        {'nombre': 'Gimnasio', 'tipo': 'Gimnasio', 'capacidad_maxima': 12, 'costo_hora': Decimal('0')},
        {'nombre': 'Zona BBQ Torre A', 'tipo': 'BBQ', 'capacidad_maxima': 20, 'costo_hora': Decimal('30000')},
        {'nombre': 'Zona BBQ Torre B', 'tipo': 'BBQ', 'capacidad_maxima': 20, 'costo_hora': Decimal('30000')},
        {'nombre': 'Parque Infantil', 'tipo': 'Juegos Infantiles', 'capacidad_maxima': 30, 'costo_hora': Decimal('0')},
        {'nombre': 'Sala de Estudio', 'tipo': 'Estudio', 'capacidad_maxima': 8, 'costo_hora': Decimal('10000')},
        {'nombre': 'Terraza Panorámica', 'tipo': 'Terraza', 'capacidad_maxima': 50, 'costo_hora': Decimal('40000')}
    ]
    
    areas_creadas = []
    for area_data in areas_data:
        tipo_nombre = area_data.pop('tipo')
        tipo_area = next((t for t in tipos_areas if t.nombre == tipo_nombre), tipos_areas[0])
        
        area = AreaComun.objects.create(
            nombre=area_data['nombre'],
            tipo=tipo_area,
            capacidad_maxima=area_data['capacidad_maxima'],
            costo_por_hora=area_data['costo_hora'],
            esta_disponible=True,
            administrador_responsable=admin_user
        )
        areas_creadas.append(area)
    
    # Crear servicios adicionales
    servicios_data = [
        {'nombre': 'Sonido Profesional', 'descripcion': 'Sistema de sonido para eventos', 'costo': Decimal('80000')},
        {'nombre': 'Decoración Básica', 'descripcion': 'Manteles y centros de mesa', 'costo': Decimal('50000')},
        {'nombre': 'Sillas Adicionales', 'descripcion': 'Sillas extra para eventos grandes', 'costo': Decimal('2000')},
        {'nombre': 'Servicio de Limpieza', 'descripcion': 'Limpieza después del evento', 'costo': Decimal('60000')},
        {'nombre': 'Seguridad Adicional', 'descripcion': 'Guardia de seguridad para eventos', 'costo': Decimal('100000')},
        {'nombre': 'Proyector y Pantalla', 'descripcion': 'Equipo audiovisual', 'costo': Decimal('40000')},
        {'nombre': 'Mesa de Ping Pong', 'descripcion': 'Mesa de ping pong portátil', 'costo': Decimal('25000')},
        {'nombre': 'Toldo Adicional', 'descripcion': 'Protección contra sol y lluvia', 'costo': Decimal('30000')},
        {'nombre': 'Catering Básico', 'descripcion': 'Servicio de refrigerios', 'costo': Decimal('15000')},
        {'nombre': 'Animación Infantil', 'descripción': 'Entretenimiento para niños', 'costo': Decimal('120000')}
    ]
    
    servicios_creados = []
    for servicio_data in servicios_data:
        servicio = ServicioAdicional.objects.create(**servicio_data)
        servicios_creados.append(servicio)
    
    # Crear algunas reservas
    residentes = list(Usuario.objects.filter(groups__name='Residentes'))
    areas = list(AreaComun.objects.all())
    
    reservas_creadas = []
    for i in range(12):
        usuario = random.choice(residentes)
        area = random.choice(areas)
        
        # Generar fechas futuras
        fecha_reserva = timezone.now() + timedelta(days=random.randint(1, 60))
        hora_inicio = fecha_reserva.replace(hour=random.randint(8, 18), minute=0, second=0, microsecond=0)
        hora_fin = hora_inicio + timedelta(hours=random.randint(1, 4))
        
        reserva = Reserva.objects.create(
            usuario=usuario,
            area_comun=area,
            fecha_reserva=fecha_reserva.date(),
            hora_inicio=hora_inicio.time(),
            hora_fin=hora_fin.time(),
            numero_invitados=random.randint(1, area.capacidad_maxima // 2),
            proposito=random.choice([
                'Cumpleaños familiar',
                'Reunión de trabajo',
                'Celebración de aniversario',
                'Actividad deportiva',
                'Estudio grupal',
                'Evento social',
                'Ejercicio personal',
                'Reunión de amigos'
            ]),
            estado='confirmada',
            observaciones='Reserva creada automáticamente'
        )
        reservas_creadas.append(reserva)
    
    print(f"📊 Tipos de área: {len(tipos_creados)}")
    print(f"📊 Áreas comunes: {len(areas_creadas)}")
    print(f"📊 Servicios adicionales: {len(servicios_creados)}")
    print(f"📊 Reservas creadas: {len(reservas_creadas)}")

def create_seguridad_data():
    """Crear datos de seguridad"""
    print("\n🔒 Creando datos de seguridad...")
    
    # Crear tipos de visitantes
    tipos_visitantes_data = [
        {'nombre': 'Familiar', 'requiere_autorizacion': False, 'tiempo_maximo_visita': 480, 'color': '#28a745'},
        {'nombre': 'Amigo', 'requiere_autorizacion': True, 'tiempo_maximo_visita': 360, 'color': '#007bff'},
        {'nombre': 'Proveedor', 'requiere_autorizacion': True, 'tiempo_maximo_visita': 180, 'color': '#ffc107'},
        {'nombre': 'Delivery', 'requiere_autorizacion': False, 'tiempo_maximo_visita': 30, 'color': '#17a2b8'},
        {'nombre': 'Técnico', 'requiere_autorizacion': True, 'tiempo_maximo_visita': 240, 'color': '#fd7e14'},
        {'nombre': 'Vendedor', 'requiere_autorizacion': True, 'tiempo_maximo_visita': 60, 'color': '#6c757d'},
        {'nombre': 'Profesional', 'requiere_autorizacion': True, 'tiempo_maximo_visita': 300, 'color': '#20c997'},
        {'nombre': 'Emergencia', 'requiere_autorizacion': False, 'tiempo_maximo_visita': 720, 'color': '#dc3545'},
        {'nombre': 'Contratista', 'requiere_autorizacion': True, 'tiempo_maximo_visita': 480, 'color': '#6f42c1'},
        {'nombre': 'Invitado Evento', 'requiere_autorizacion': True, 'tiempo_maximo_visita': 600, 'color': '#e83e8c'}
    ]
    
    tipos_creados = []
    for tipo_data in tipos_visitantes_data:
        tipo, created = TipoVisitante.objects.get_or_create(
            nombre=tipo_data['nombre'],
            defaults=tipo_data
        )
        if created:
            tipos_creados.append(tipo)
    
    # Crear configuraciones de IA
    admin_user = Usuario.objects.filter(is_staff=True).first()
    
    configs_ia_data = [
        {
            'nombre': 'Reconocimiento Facial Visitantes',
            'tipo_algoritmo': 'face_recognition',
            'descripcion': 'Sistema de reconocimiento facial para visitantes',
            'modelo_ia': 'face_recognition_v2.model',
            'umbral_confianza': Decimal('85.00')
        },
        {
            'nombre': 'OCR Placas Vehiculares',
            'tipo_algoritmo': 'license_plate_ocr',
            'descripcion': 'Reconocimiento de placas de vehículos',
            'modelo_ia': 'license_plate_ocr_v1.model',
            'umbral_confianza': Decimal('90.00')
        },
        {
            'nombre': 'Detección de Anomalías',
            'tipo_algoritmo': 'anomaly_detection',
            'descripcion': 'Detección de comportamientos anómalos',
            'modelo_ia': 'anomaly_detection_v1.model',
            'umbral_confianza': Decimal('75.00')
        },
        {
            'nombre': 'Detección de Objetos Peligrosos',
            'tipo_algoritmo': 'object_detection',
            'descripcion': 'Identificación de objetos potencialmente peligrosos',
            'modelo_ia': 'object_detection_v2.model',
            'umbral_confianza': Decimal('80.00')
        },
        {
            'nombre': 'Análisis de Comportamiento',
            'tipo_algoritmo': 'behavioral_analysis',
            'descripcion': 'Análisis de patrones de comportamiento',
            'modelo_ia': 'behavioral_analysis_v1.model',
            'umbral_confianza': Decimal('70.00')
        },
        {
            'nombre': 'Predicción de Morosidad',
            'tipo_algoritmo': 'predictive_analytics',
            'descripcion': 'Predicción de riesgo de morosidad',
            'modelo_ia': 'morosidad_prediction_v1.model',
            'umbral_confianza': Decimal('82.00')
        }
    ]
    
    configs_creadas = []
    for config_data in configs_ia_data:
        config = ConfiguracionIA.objects.create(
            **config_data,
            creado_por=admin_user,
            parametros_configuracion={
                'learning_rate': 0.001,
                'batch_size': 32,
                'epochs': 100
            }
        )
        configs_creadas.append(config)
    
    # Crear registros de visitantes
    tipos_visitantes = list(TipoVisitante.objects.all())
    unidades = list(UnidadHabitacional.objects.all())
    usuarios_seguridad = list(Usuario.objects.filter(groups__name='Seguridad'))
    
    visitantes_data = [
        {'nombres': 'Ana María', 'apellidos': 'Rodriguez Silva', 'documento_identidad': '12345678', 'telefono': '+1-555-1001'},
        {'nombres': 'Carlos Eduardo', 'apellidos': 'López Méndez', 'documento_identidad': '23456789', 'telefono': '+1-555-1002'},
        {'nombres': 'Sofia Elena', 'apellidos': 'García Torres', 'documento_identidad': '34567890', 'telefono': '+1-555-1003'},
        {'nombres': 'Miguel Alejandro', 'apellidos': 'Herrera Castro', 'documento_identidad': '45678901', 'telefono': '+1-555-1004'},
        {'nombres': 'Laura Patricia', 'apellidos': 'Vargas Ruiz', 'documento_identidad': '56789012', 'telefono': '+1-555-1005'},
        {'nombres': 'Diego Fernando', 'apellidos': 'Morales Jiménez', 'documento_identidad': '67890123', 'telefono': '+1-555-1006'},
        {'nombres': 'Valentina', 'apellidos': 'Sánchez Rivera', 'documento_identidad': '78901234', 'telefono': '+1-555-1007'},
        {'nombres': 'Andrés Felipe', 'apellidos': 'Torres Delgado', 'documento_identidad': '89012345', 'telefono': '+1-555-1008'},
        {'nombres': 'Camila Andrea', 'apellidos': 'Ramírez Peña', 'documento_identidad': '90123456', 'telefono': '+1-555-1009'},
        {'nombres': 'Sebastian', 'apellidos': 'Cruz Martínez', 'documento_identidad': '01234567', 'telefono': '+1-555-1010'}
    ]
    
    visitantes_creados = []
    for i, visitante_data in enumerate(visitantes_data):
        unidad = random.choice(unidades)
        tipo_visitante = random.choice(tipos_visitantes)
        usuario_seguridad = random.choice(usuarios_seguridad) if usuarios_seguridad else admin_user
        
        # Generar fechas de visita (algunas pasadas, algunas futuras)
        fecha_base = timezone.now() + timedelta(days=random.randint(-30, 30))
        
        visitante = RegistroVisitante.objects.create(
            nombres=visitante_data['nombres'],
            apellidos=visitante_data['apellidos'],
            documento_identidad=visitante_data['documento_identidad'],
            telefono=visitante_data['telefono'],
            tipo_visitante=tipo_visitante,
            unidad_destino=unidad,
            motivo_visita=random.choice([
                'Visita familiar',
                'Reunión de trabajo desde casa',
                'Entrega de paquete',
                'Servicio técnico',
                'Visita médica a domicilio',
                'Celebración familiar',
                'Reunión de amigos',
                'Servicio de limpieza'
            ]),
            estado=random.choice(['pendiente', 'autorizado', 'finalizado']),
            registrado_por=usuario_seguridad,
            fecha_ingreso=fecha_base if random.choice([True, False]) else None
        )
        visitantes_creados.append(visitante)
    
    # Crear vehículos
    residentes = list(Usuario.objects.filter(groups__name='Residentes'))
    
    vehiculos_data = [
        {'placa': 'ABC123', 'tipo': 'auto', 'marca': 'Toyota', 'modelo': 'Corolla', 'color': 'Blanco', 'año': 2020},
        {'placa': 'DEF456', 'tipo': 'camioneta', 'marca': 'Chevrolet', 'modelo': 'Captiva', 'color': 'Negro', 'año': 2019},
        {'placa': 'GHI789', 'tipo': 'auto', 'marca': 'Nissan', 'modelo': 'Sentra', 'color': 'Gris', 'año': 2021},
        {'placa': 'JKL012', 'tipo': 'moto', 'marca': 'Yamaha', 'modelo': 'FZ', 'color': 'Azul', 'año': 2018},
        {'placa': 'MNO345', 'tipo': 'auto', 'marca': 'Hyundai', 'modelo': 'Accent', 'color': 'Rojo', 'año': 2022},
        {'placa': 'PQR678', 'tipo': 'camioneta', 'marca': 'Ford', 'modelo': 'Ranger', 'color': 'Verde', 'año': 2020},
        {'placa': 'STU901', 'tipo': 'auto', 'marca': 'Renault', 'modelo': 'Logan', 'color': 'Plata', 'año': 2019},
        {'placa': 'VWX234', 'tipo': 'moto', 'marca': 'Honda', 'modelo': 'CB', 'color': 'Negro', 'año': 2021},
        {'placa': 'YZA567', 'tipo': 'auto', 'marca': 'Kia', 'modelo': 'Rio', 'color': 'Blanco', 'año': 2020},
        {'placa': 'BCD890', 'tipo': 'van', 'marca': 'Chevrolet', 'modelo': 'N300', 'color': 'Azul', 'año': 2018}
    ]
    
    vehiculos_creados = []
    for i, vehiculo_data in enumerate(vehiculos_data):
        if i < len(residentes) and i < len(unidades):
            vehiculo = AccesoVehiculo.objects.create(
                placa_vehiculo=vehiculo_data['placa'],
                tipo_vehiculo=vehiculo_data['tipo'],
                marca=vehiculo_data['marca'],
                modelo=vehiculo_data['modelo'],
                color=vehiculo_data['color'],
                año=vehiculo_data['año'],
                propietario=residentes[i],
                unidad_asignada=unidades[i],
                estado_acceso='autorizado',
                registrado_por=usuarios_seguridad[0] if usuarios_seguridad else admin_user
            )
            vehiculos_creados.append(vehiculo)
    
    print(f"📊 Tipos de visitantes: {len(tipos_creados)}")
    print(f"📊 Configuraciones IA: {len(configs_creadas)}")
    print(f"📊 Visitantes registrados: {len(visitantes_creados)}")
    print(f"📊 Vehículos registrados: {len(vehiculos_creados)}")

def main():
    """Función principal para poblar la base de datos"""
    print("🚀 INICIANDO POBLACIÓN DE LA BASE DE DATOS")
    print("=" * 60)
    
    try:
        # Crear usuarios y perfiles
        usuarios = create_usuarios_and_perfiles()
        
        # Crear unidades habitacionales
        unidades = create_unidades_habitacionales()
        
        # Crear datos financieros
        create_finanzas_data()
        
        # Crear datos de comunicación
        create_comunicacion_data()
        
        # Crear datos de reservas
        create_reservas_data()
        
        # Crear datos de seguridad
        create_seguridad_data()
        
        print("\n" + "=" * 60)
        print("✅ ¡BASE DE DATOS POBLADA EXITOSAMENTE!")
        print("=" * 60)
        
        # Resumen final
        print("\n📊 RESUMEN FINAL:")
        print(f"👥 Usuarios: {Usuario.objects.count()}")
        print(f"🏠 Unidades: {UnidadHabitacional.objects.count()}")
        print(f"💰 Pagos: {Pago.objects.count()}")
        print(f"📢 Avisos: {AvisoGeneral.objects.count()}")
        print(f"📅 Reservas: {Reserva.objects.count()}")
        print(f"🏊‍♂️ Áreas comunes: {AreaComun.objects.count()}")
        print(f"👤 Visitantes: {RegistroVisitante.objects.count()}")
        print(f"🚗 Vehículos: {AccesoVehiculo.objects.count()}")
        
        print("\n🎉 ¡Listo para usar el Smart Condominium!")
        
    except Exception as e:
        print(f"❌ Error durante la población: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()