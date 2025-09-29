from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    TipoAreaComun, AreaComun, Reserva, ImagenAreaComun,
    ServicioAdicional, ReservaServicio, DisponibilidadEspecial
)
from .serializers import (
    SerializadorTipoAreaComun, SerializadorAreaComun, SerializadorAreaComunSimple,
    SerializadorReserva, SerializadorCrearReserva, SerializadorDisponibilidad,
    SerializadorHorarioDisponible, SerializadorServicioAdicional,
    SerializadorDisponibilidadEspecial, SerializadorEstadisticasReservas
)
from apps.finanzas.models import UnidadHabitacional

class ListaTiposAreaComun(generics.ListCreateAPIView):
    """
    Listar y crear tipos de áreas comunes
    """
    queryset = TipoAreaComun.objects.filter(esta_activo=True)
    serializer_class = SerializadorTipoAreaComun
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TipoAreaComun.objects.filter(esta_activo=True).order_by('orden', 'nombre')

class ListaAreasComunes(generics.ListAPIView):
    """
    Listar áreas comunes disponibles (Caso de Uso 8: Consultar disponibilidad)
    """
    serializer_class = SerializadorAreaComunSimple
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = AreaComun.objects.filter(permite_reservas=True)
        
        # Filtros opcionales
        tipo_area = self.request.query_params.get('tipo_area')
        if tipo_area:
            queryset = queryset.filter(tipo_area_id=tipo_area)
        
        solo_disponibles = self.request.query_params.get('solo_disponibles', 'false')
        if solo_disponibles.lower() == 'true':
            queryset = queryset.filter(estado='disponible')
        
        capacidad_minima = self.request.query_params.get('capacidad_minima')
        if capacidad_minima:
            queryset = queryset.filter(capacidad_maxima__gte=capacidad_minima)
        
        # Búsqueda por texto
        busqueda = self.request.query_params.get('buscar')
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripcion__icontains=busqueda) |
                Q(ubicacion__icontains=busqueda)
            )
        
        return queryset.order_by('tipo_area__orden', 'nombre')

class DetalleAreaComun(generics.RetrieveAPIView):
    """
    Ver detalles de un área común específica
    """
    queryset = AreaComun.objects.filter(permite_reservas=True)
    serializer_class = SerializadorAreaComun
    permission_classes = [permissions.IsAuthenticated]

# Vistas de Administración (Casos de Uso 15 y 16)
class ListaAreasAdministrador(generics.ListCreateAPIView):
    """
    Listar y crear áreas comunes (Caso de Uso 15: Configurar áreas comunes)
    Solo para administradores
    """
    queryset = AreaComun.objects.all()
    serializer_class = SerializadorAreaComun
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Solo administradores pueden acceder")
        return AreaComun.objects.all().order_by('tipo_area__orden', 'nombre')
    
    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Solo administradores pueden crear áreas")
        serializer.save(creado_por=self.request.user)

class DetalleAreaAdministrador(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar área común (Caso de Uso 16: Gestionar tarifas)
    Solo para administradores
    """
    queryset = AreaComun.objects.all()
    serializer_class = SerializadorAreaComun
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Solo administradores pueden acceder")
        return super().get_object()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def consultar_disponibilidad(request):
    """
    Consultar disponibilidad de un área en una fecha específica
    (Caso de Uso 8: Consultar disponibilidad de áreas comunes)
    """
    serializador = SerializadorDisponibilidad(data=request.query_params)
    if not serializador.is_valid():
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    
    area_comun_id = serializador.validated_data['area_comun_id']
    fecha = serializador.validated_data['fecha']
    
    try:
        area_comun = AreaComun.objects.get(id=area_comun_id)
    except AreaComun.DoesNotExist:
        return Response({
            'error': 'Área común no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verificar disponibilidad general del área
    if not area_comun.esta_disponible:
        return Response({
            'disponible': False,
            'motivo': f'El área está {area_comun.get_estado_display()}',
            'horarios_disponibles': []
        })
    
    # Obtener horarios de funcionamiento para el día
    dia_semana = [
        'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'
    ][fecha.weekday()]
    
    horario_dia = area_comun.horario_funcionamiento.get(dia_semana, {})
    if not horario_dia.get('activo', False):
        return Response({
            'disponible': False,
            'motivo': 'El área no está disponible este día de la semana',
            'horarios_disponibles': []
        })
    
    hora_inicio_str = horario_dia.get('inicio', '08:00')
    hora_fin_str = horario_dia.get('fin', '22:00')
    
    # Convertir a objetos time
    hora_inicio_area = datetime.strptime(hora_inicio_str, '%H:%M').time()
    hora_fin_area = datetime.strptime(hora_fin_str, '%H:%M').time()
    
    # Obtener reservas existentes para esa fecha
    reservas_existentes = Reserva.objects.filter(
        area_comun=area_comun,
        fecha_reserva=fecha,
        estado__in=['confirmada', 'en_uso', 'pendiente']
    ).order_by('hora_inicio')
    
    # Generar horarios disponibles (cada hora)
    horarios_disponibles = []
    hora_actual = hora_inicio_area
    
    while hora_actual < hora_fin_area:
        # Calcular hora de fin (mínimo 1 hora)
        hora_fin_slot = (
            datetime.combine(fecha, hora_actual) + 
            timedelta(hours=1)
        ).time()
        
        if hora_fin_slot > hora_fin_area:
            break
        
        # Verificar si hay conflicto con reservas existentes
        conflicto = False
        motivo_conflicto = ""
        
        for reserva in reservas_existentes:
            if not (hora_fin_slot <= reserva.hora_inicio or hora_actual >= reserva.hora_fin):
                conflicto = True
                motivo_conflicto = f"Reservado ({reserva.codigo_reserva})"
                break
        
        horarios_disponibles.append({
            'hora_inicio': hora_actual.strftime('%H:%M'),
            'hora_fin': hora_fin_slot.strftime('%H:%M'),
            'disponible': not conflicto,
            'motivo': motivo_conflicto if conflicto else 'Disponible'
        })
        
        # Avanzar una hora
        hora_actual = (
            datetime.combine(fecha, hora_actual) + 
            timedelta(hours=1)
        ).time()
    
    return Response({
        'area_comun': {
            'id': area_comun.id,
            'nombre': area_comun.nombre,
            'capacidad_maxima': area_comun.capacidad_maxima,
            'tarifa_actual': area_comun.tarifa_actual
        },
        'fecha': fecha,
        'disponible': len([h for h in horarios_disponibles if h['disponible']]) > 0,
        'horarios_disponibles': horarios_disponibles,
        'horario_funcionamiento': {
            'inicio': hora_inicio_str,
            'fin': hora_fin_str
        }
    })

class ListaReservasUsuario(generics.ListAPIView):
    """
    Listar reservas del usuario autenticado
    """
    serializer_class = SerializadorReserva
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        usuario = self.request.user
        queryset = Reserva.objects.filter(usuario=usuario)
        
        # Filtros opcionales
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        desde = self.request.query_params.get('desde')
        if desde:
            queryset = queryset.filter(fecha_reserva__gte=desde)
        
        hasta = self.request.query_params.get('hasta')
        if hasta:
            queryset = queryset.filter(fecha_reserva__lte=hasta)
        
        return queryset.order_by('-fecha_creacion')

class CrearReserva(generics.CreateAPIView):
    """
    Crear nueva reserva (Caso de Uso 6: Hacer reservas de áreas comunes)
    """
    serializer_class = SerializadorCrearReserva
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Verificar que el usuario tenga una unidad asociada
        usuario = request.user
        unidad = UnidadHabitacional.objects.filter(
            Q(propietario=usuario) | Q(inquilino=usuario)
        ).first()
        
        if not unidad:
            return Response({
                'error': 'No tiene una unidad asociada para realizar reservas'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_201_CREATED:
            reserva = Reserva.objects.get(id=response.data['id'])
            
            # Crear notificación si es necesario
            try:
                from apps.comunicacion.models import Notificacion, CategoriaNotificacion
                
                categoria, _ = CategoriaNotificacion.objects.get_or_create(
                    nombre='Reservas',
                    defaults={'descripcion': 'Notificaciones sobre reservas de áreas comunes'}
                )
                
                if reserva.requiere_aprobacion:
                    titulo = f"Reserva pendiente de aprobación - {reserva.codigo_reserva}"
                    mensaje = f"Su reserva del área {reserva.area_comun.nombre} está pendiente de aprobación."
                else:
                    titulo = f"Reserva confirmada - {reserva.codigo_reserva}"
                    mensaje = f"Su reserva del área {reserva.area_comun.nombre} ha sido confirmada."
                
                Notificacion.objects.create(
                    titulo=titulo,
                    mensaje=mensaje,
                    categoria=categoria,
                    tipo_destinatario='usuarios',
                    es_push=True,
                    creado_por=usuario,
                    estado='enviada'
                )
                
            except Exception as e:
                # No fallar la creación por error en notificación
                print(f"Error creando notificación: {e}")
        
        return response

class DetalleReserva(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o cancelar reserva específica
    """
    queryset = Reserva.objects.all()
    serializer_class = SerializadorReserva
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_staff:
            return Reserva.objects.all()
        return Reserva.objects.filter(usuario=usuario)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def aprobar_reserva(request, reserva_id):
    if not request.user.is_staff:
        return Response({
            'error': 'Solo administradores pueden aprobar reservas'
        }, status=status.HTTP_403_FORBIDDEN)
    try:
        reserva = Reserva.objects.get(id=reserva_id, estado='pendiente')
    except Reserva.DoesNotExist:
        return Response({
            'error': 'Reserva no encontrada o no está pendiente'
        }, status=status.HTTP_404_NOT_FOUND)

    accion = request.data.get('accion')  # 'aprobar' o 'rechazar'
    observaciones = request.data.get('observaciones', '')

    if accion == 'aprobar':
        reserva.estado = 'confirmada'
        reserva.aprobado_por = request.user
        reserva.fecha_aprobacion = timezone.now()
        mensaje = f"Reserva {reserva.codigo_reserva} aprobada exitosamente"
        
    elif accion == 'rechazar':
        reserva.estado = 'cancelada_admin'
        reserva.motivo_cancelacion = observaciones or 'Rechazada por administración'
        mensaje = f"Reserva {reserva.codigo_reserva} rechazada"
        
    else:
        return Response({
            'error': 'Acción inválida. Use "aprobar" o "rechazar"'
        }, status=status.HTTP_400_BAD_REQUEST)

    reserva.observaciones_admin = observaciones
    reserva.save()

    # Crear notificación para el usuario
    try:
        from apps.comunicacion.models import Notificacion, CategoriaNotificacion
        
        categoria, _ = CategoriaNotificacion.objects.get_or_create(
            nombre='Reservas',
            defaults={'descripcion': 'Notificaciones sobre reservas de áreas comunes'}
        )
        
        if accion == 'aprobar':
            titulo = f"Reserva aprobada - {reserva.codigo_reserva}"
            mensaje_notif = f"Su reserva del área {reserva.area_comun.nombre} ha sido aprobada."
        else:
            titulo = f"Reserva rechazada - {reserva.codigo_reserva}"
            mensaje_notif = f"Su reserva del área {reserva.area_comun.nombre} ha sido rechazada. Motivo: {observaciones}"
        
        Notificacion.objects.create(
            titulo=titulo,
            mensaje=mensaje_notif,
            categoria=categoria,
            tipo_destinatario='usuarios',
            es_push=True,
            creado_por=request.user,
            estado='enviada'
        )
        
    except Exception as e:
        print(f"Error creando notificación: {e}")

    return Response({
        'mensaje': mensaje,
        'reserva': SerializadorReserva(reserva).data
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def calificar_reserva(request, reserva_id):
    try:
        reserva = Reserva.objects.get(
            id=reserva_id,
            usuario=request.user,
            estado='completada'
        )
    except Reserva.DoesNotExist:
        return Response({
            'error': 'Reserva no encontrada o no está completada'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if reserva.calificacion:
        return Response({
            'error': 'Esta reserva ya ha sido calificada'
        }, status=status.HTTP_400_BAD_REQUEST)

    calificacion = request.data.get('calificacion')
    comentario = request.data.get('comentario', '')

    if not calificacion or calificacion < 1 or calificacion > 5:
        return Response({
            'error': 'La calificación debe ser entre 1 y 5'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Guardar calificación
    reserva.calificacion = calificacion
    reserva.comentario_calificacion = comentario
    reserva.fecha_calificacion = timezone.now()
    reserva.save()

    # Actualizar rating promedio del área
    area_comun = reserva.area_comun
    calificaciones = Reserva.objects.filter(
        area_comun=area_comun,
        calificacion__isnull=False
    ).aggregate(
        promedio=Avg('calificacion'),
        total=Count('calificacion')
    )

    area_comun.rating_promedio = calificaciones['promedio'] or 0
    area_comun.save()

    return Response({
        'mensaje': 'Calificación guardada exitosamente',
        'calificacion': calificacion,
        'rating_promedio_area': area_comun.rating_promedio
    })

class ListaReservasAdministrador(generics.ListAPIView):
    """
    Listar todas las reservas (solo administradores)
    """
    serializer_class = SerializadorReserva
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Solo administradores pueden acceder")
        
        queryset = Reserva.objects.all()
        
        # Filtros
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        area_comun = self.request.query_params.get('area_comun')
        if area_comun:
            queryset = queryset.filter(area_comun_id=area_comun)
        
        desde = self.request.query_params.get('desde')
        if desde:
            queryset = queryset.filter(fecha_reserva__gte=desde)
        
        hasta = self.request.query_params.get('hasta')
        if hasta:
            queryset = queryset.filter(fecha_reserva__lte=hasta)
        
        pendientes = self.request.query_params.get('pendientes')
        if pendientes == 'true':
            queryset = queryset.filter(estado='pendiente')
        
        return queryset.order_by('-fecha_creacion')
class ListaServiciosAdicionales(generics.ListCreateAPIView):
    """
    Listar y crear servicios adicionales
    """
    queryset = ServicioAdicional.objects.filter(esta_activo=True)
    serializer_class = SerializadorServicioAdicional
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = ServicioAdicional.objects.filter(esta_activo=True)
        
        area_comun = self.request.query_params.get('area_comun')
        if area_comun:
            queryset = queryset.filter(areas_aplicables__id=area_comun)
        
        return queryset.order_by('nombre')

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Solo administradores pueden crear servicios")
        serializer.save()
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def horarios_ocupados(request):
    """
    Obtener horarios ocupados de un área común en un rango de fechas
    """
    area_comun_id = request.query_params.get('area_comun')
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin', fecha_inicio)
    
    if not area_comun_id or not fecha_inicio:
        return Response({
            'error': 'Se requieren area_comun y fecha_inicio'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        area_comun = AreaComun.objects.get(id=area_comun_id)
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    except (AreaComun.DoesNotExist, ValueError):
        return Response({
            'error': 'Área común no encontrada o fecha inválida'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Obtener reservas en el rango de fechas
    reservas = Reserva.objects.filter(
        area_comun=area_comun,
        fecha_reserva__range=[fecha_inicio, fecha_fin],
        estado__in=['confirmada', 'en_uso', 'pendiente']
    ).order_by('fecha_reserva', 'hora_inicio')

    horarios_ocupados = []
    for reserva in reservas:
        horarios_ocupados.append({
            'fecha': reserva.fecha_reserva,
            'hora_inicio': reserva.hora_inicio,
            'hora_fin': reserva.hora_fin,
            'codigo_reserva': reserva.codigo_reserva,
            'nombre_evento': reserva.nombre_evento,
            'estado': reserva.estado
        })

    return Response({
        'area_comun': area_comun.nombre,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'horarios_ocupados': horarios_ocupados
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def estadisticas_reservas(request):
    """
    Obtener estadísticas de reservas
    """
    usuario = request.user
    
    if usuario.is_staff:
        # Estadísticas completas para administradores
        total_reservas = Reserva.objects.count()
        reservas_confirmadas = Reserva.objects.filter(estado='confirmada').count()
        reservas_pendientes = Reserva.objects.filter(estado='pendiente').count()
        reservas_canceladas = Reserva.objects.filter(estado__in=['cancelada_usuario', 'cancelada_admin']).count()
        reservas_completadas = Reserva.objects.filter(estado='completada').count()
        
        # Ingresos del mes actual
        mes_actual = timezone.now().replace(day=1)
        ingresos_mes = Reserva.objects.filter(
            fecha_creacion__gte=mes_actual,
            estado__in=['confirmada', 'completada']
        ).aggregate(
            total=Sum('costo_total')
        )['total'] or 0
        
        # Área más popular
        area_popular = AreaComun.objects.annotate(
            num_reservas=Count('reservas')
        ).order_by('-num_reservas').first()
        
        # Horario más solicitado
        reservas_por_hora = Reserva.objects.filter(
            estado__in=['confirmada', 'completada']
        ).extra({
            'hora': "EXTRACT(hour FROM hora_inicio)"
        }).values('hora').annotate(
            count=Count('id')
        ).order_by('-count').first()
        
        horario_popular = f"{int(reservas_por_hora['hora']):02d}:00" if reservas_por_hora else "N/A"
        
        # Reservas por tipo de evento
        reservas_por_tipo = Reserva.objects.values('tipo_evento').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Tasa de ocupación (simplificada)
        dias_mes = timezone.now().day
        areas_disponibles = AreaComun.objects.filter(permite_reservas=True).count()
        tasa_ocupacion = (total_reservas / max(dias_mes * areas_disponibles, 1)) * 100
        
    else:
        # Estadísticas del usuario
        reservas_usuario = Reserva.objects.filter(usuario=usuario)
        total_reservas = reservas_usuario.count()
        reservas_confirmadas = reservas_usuario.filter(estado='confirmada').count()
        reservas_pendientes = reservas_usuario.filter(estado='pendiente').count()
        reservas_canceladas = reservas_usuario.filter(estado__in=['cancelada_usuario', 'cancelada_admin']).count()
        reservas_completadas = reservas_usuario.filter(estado='completada').count()
        
        ingresos_mes = reservas_usuario.filter(
            estado__in=['confirmada', 'completada']
        ).aggregate(
            total=Sum('costo_total')
        )['total'] or 0
        
        area_popular_usuario = reservas_usuario.values('area_comun__nombre').annotate(
            count=Count('id')
        ).order_by('-count').first()
        
        area_popular = area_popular_usuario['area_comun__nombre'] if area_popular_usuario else "N/A"
        horario_popular = "N/A"  # Simplificado para usuario
        tasa_ocupacion = 0
        reservas_por_tipo = reservas_usuario.values('tipo_evento').annotate(
            count=Count('id')
        ).order_by('-count')

    # Reservas recientes
    reservas_recientes = Reserva.objects.filter(
        usuario=usuario if not usuario.is_staff else None
    ).order_by('-fecha_creacion')[:5]

    if usuario.is_staff:
        reservas_recientes = Reserva.objects.all().order_by('-fecha_creacion')[:5]

    datos = {
        'total_reservas': total_reservas,
        'reservas_confirmadas': reservas_confirmadas,
        'reservas_pendientes': reservas_pendientes,
        'reservas_canceladas': reservas_canceladas,
        'reservas_completadas': reservas_completadas,
        'tasa_ocupacion': round(tasa_ocupacion, 2),
        'ingresos_mes_actual': ingresos_mes,
        'area_mas_popular': area_popular.nombre if hasattr(area_popular, 'nombre') else area_popular,
        'horario_mas_solicitado': horario_popular,
        'reservas_por_tipo_evento': list(reservas_por_tipo),
        'reservas_recientes': SerializadorReserva(reservas_recientes, many=True).data
    }

    return Response(datos)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def crear_disponibilidad_especial(request):
    """
    Crear disponibilidad especial para un área común
    """
    if not request.user.is_staff:
        return Response({
            'error': 'Solo administradores pueden crear disponibilidades especiales'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializador = SerializadorDisponibilidadEspecial(data=request.data)
    if serializador.is_valid():
        disponibilidad = serializador.save(creado_por=request.user)
        return Response(
            SerializadorDisponibilidadEspecial(disponibilidad).data,
            status=status.HTTP_201_CREATED
        )

    return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def calendario_reservas(request):
    """
    Obtener calendario de reservas para un área común
    """
    area_comun_id = request.query_params.get('area_comun')
    mes = request.query_params.get('mes')  # Formato: YYYY-MM
    
    if not area_comun_id:
        return Response({
            'error': 'Se requiere el parámetro area_comun'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        area_comun = AreaComun.objects.get(id=area_comun_id)
    except AreaComun.DoesNotExist:
        return Response({
            'error': 'Área común no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)

    # Determinar rango de fechas
    if mes:
        try:
            fecha_inicio = datetime.strptime(mes + '-01', '%Y-%m-%d').date()
            # Último día del mes
            if fecha_inicio.month == 12:
                fecha_fin = fecha_inicio.replace(year=fecha_inicio.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                fecha_fin = fecha_inicio.replace(month=fecha_inicio.month + 1, day=1) - timedelta(days=1)
        except ValueError:
            return Response({
                'error': 'Formato de mes inválido. Use YYYY-MM'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Mes actual por defecto
        hoy = timezone.now().date()
        fecha_inicio = hoy.replace(day=1)
        if fecha_inicio.month == 12:
            fecha_fin = fecha_inicio.replace(year=fecha_inicio.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            fecha_fin = fecha_inicio.replace(month=fecha_inicio.month + 1, day=1) - timedelta(days=1)

    # Obtener reservas del período
    reservas = Reserva.objects.filter(
        area_comun=area_comun,
        fecha_reserva__range=[fecha_inicio, fecha_fin]
    ).exclude(
        estado__in=['cancelada_usuario', 'cancelada_admin']
    ).order_by('fecha_reserva', 'hora_inicio')

    # Agrupar reservas por día
    calendario = {}
    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:
        calendario[fecha_actual.isoformat()] = {
            'fecha': fecha_actual,
            'dia_semana': fecha_actual.strftime('%A'),
            'reservas': [],
            'disponible': area_comun.esta_disponible_en_horario(
                datetime.combine(fecha_actual, datetime.min.time())
            )
        }
        fecha_actual += timedelta(days=1)

    # Agregar reservas al calendario
    for reserva in reservas:
        fecha_str = reserva.fecha_reserva.isoformat()
        if fecha_str in calendario:
            calendario[fecha_str]['reservas'].append({
                'id': reserva.id,
                'codigo_reserva': reserva.codigo_reserva,
                'nombre_evento': reserva.nombre_evento,
                'hora_inicio': reserva.hora_inicio,
                'hora_fin': reserva.hora_fin,
                'estado': reserva.estado,
                'usuario': reserva.usuario.get_full_name(),
                'numero_invitados': reserva.numero_invitados
            })

    return Response({
        'area_comun': {
            'id': area_comun.id,
            'nombre': area_comun.nombre,
            'capacidad_maxima': area_comun.capacidad_maxima
        },
        'periodo': {
            'inicio': fecha_inicio,
            'fin': fecha_fin,
            'mes': fecha_inicio.strftime('%B %Y')
        },
        'calendario': calendario
    })
