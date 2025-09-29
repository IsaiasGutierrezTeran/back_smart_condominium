
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import (
    CategoriaNotificacion, Notificacion, DestinatarioNotificacion,
    AvisoGeneral, InteraccionAviso, ConfiguracionNotificacion,
    PlantillaNotificacion
)
from .serializers import (
    SerializadorCategoriaNotificacion, SerializadorNotificacion,
    SerializadorCrearNotificacion, SerializadorAvisoGeneral,
    SerializadorInteraccionAviso, SerializadorConfiguracionNotificacion,
    SerializadorPlantillaNotificacion, SerializadorRenderizarPlantilla,
    SerializadorNotificacionUsuario, SerializadorEstadisticasNotificacion
)
from .services import NotificationService
from apps.autenticacion.models import Usuario
from apps.finanzas.models import UnidadHabitacional

class ListaCategorias(generics.ListCreateAPIView):
    """
    Listar y crear categorías de notificaciones
    """
    queryset = CategoriaNotificacion.objects.filter(esta_activa=True)
    serializer_class = SerializadorCategoriaNotificacion
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Solo administradores pueden crear categorías
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Solo administradores pueden crear categorías")
        serializer.save()

class DetalleCategoria(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar categoría
    """
    queryset = CategoriaNotificacion.objects.all()
    serializer_class = SerializadorCategoriaNotificacion
    permission_classes = [permissions.IsAuthenticated]

class ListaNotificacionesAdmin(generics.ListCreateAPIView):
    """
    Listar y crear notificaciones (solo administradores)
    """
    queryset = Notificacion.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SerializadorCrearNotificacion
        return SerializadorNotificacion
    
    def get_queryset(self):
        # Solo administradores pueden ver todas las notificaciones
        if not self.request.user.is_staff:
            return Notificacion.objects.filter(creado_por=self.request.user)
        
        queryset = Notificacion.objects.all()
        
        # Filtros opcionales
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
            
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
            
        urgente = self.request.query_params.get('urgente')
        if urgente == 'true':
            queryset = queryset.filter(es_urgente=True)
        
        return queryset.order_by('-fecha_creacion')

class DetalleNotificacion(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar notificación específica
    """
    queryset = Notificacion.objects.all()
    serializer_class = SerializadorNotificacion
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enviar_notificacion(request, notificacion_id):
    """
    Enviar una notificación específica
    """
    try:
        notificacion = Notificacion.objects.get(id=notificacion_id)
    except Notificacion.DoesNotExist:
        return Response({
            'error': 'Notificación no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Solo el creador o administradores pueden enviar
    if notificacion.creado_por != request.user and not request.user.is_staff:
        return Response({
            'error': 'Sin permisos para enviar esta notificación'
        }, status=status.HTTP_403_FORBIDDEN)
    
    if notificacion.estado != 'borrador':
        return Response({
            'error': 'Solo se pueden enviar notificaciones en estado borrador'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Usar el servicio de notificaciones
        resultado = NotificationService.enviar_notificacion(notificacion)
        
        return Response({
            'mensaje': 'Notificación enviada exitosamente',
            'destinatarios_procesados': resultado['total_destinatarios'],
            'enviados_exitosos': resultado['enviados_exitosos'],
            'errores': resultado['errores']
        })
        
    except Exception as e:
        return Response({
            'error': f'Error al enviar notificación: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mis_notificaciones(request):
    """
    Obtener notificaciones del usuario autenticado
    """
    usuario = request.user
    
    # Parámetros de filtro
    estado = request.query_params.get('estado', 'all')
    limite = int(request.query_params.get('limite', 20))
    solo_no_leidas = request.query_params.get('no_leidas', 'false') == 'true'
    
    # Obtener notificaciones del usuario
    queryset = DestinatarioNotificacion.objects.filter(
        usuario=usuario
    ).select_related('notificacion', 'notificacion__categoria')
    
    if estado != 'all':
        queryset = queryset.filter(estado=estado)
    
    if solo_no_leidas:
        queryset = queryset.filter(fecha_lectura__isnull=True)
    
    queryset = queryset.order_by('-fecha_envio')[:limite]
    
    serializador = SerializadorNotificacionUsuario(queryset, many=True)
    
    return Response({
        'notificaciones': serializador.data,
        'total': queryset.count(),
        'no_leidas': DestinatarioNotificacion.objects.filter(
            usuario=usuario, 
            fecha_lectura__isnull=True
        ).count()
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def marcar_como_leida(request, notificacion_id):
    """
    Marcar notificación como leída
    """
    try:
        destinatario = DestinatarioNotificacion.objects.get(
            notificacion_id=notificacion_id,
            usuario=request.user
        )
        
        if not destinatario.fecha_lectura:
            destinatario.fecha_lectura = timezone.now()
            destinatario.estado = 'leido'
            destinatario.dispositivo_lectura = request.data.get('dispositivo', 'web')
            destinatario.save()
            
            # Actualizar contador en la notificación
            notificacion = destinatario.notificacion
            notificacion.total_leidos = notificacion.destinatarios.filter(
                fecha_lectura__isnull=False
            ).count()
            notificacion.save()
        
        return Response({'mensaje': 'Notificación marcada como leída'})
        
    except DestinatarioNotificacion.DoesNotExist:
        return Response({
            'error': 'Notificación no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirmar_notificacion(request, notificacion_id):
    """
    Confirmar recepción de notificación (si requiere confirmación)
    """
    try:
        destinatario = DestinatarioNotificacion.objects.get(
            notificacion_id=notificacion_id,
            usuario=request.user
        )
        
        if not destinatario.notificacion.requiere_confirmacion:
            return Response({
                'error': 'Esta notificación no requiere confirmación'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not destinatario.fecha_confirmacion:
            destinatario.fecha_confirmacion = timezone.now()
            destinatario.estado = 'confirmado'
            destinatario.save()
            
            # Actualizar contador en la notificación
            notificacion = destinatario.notificacion
            notificacion.total_confirmados = notificacion.destinatarios.filter(
                fecha_confirmacion__isnull=False
            ).count()
            notificacion.save()
        
        return Response({'mensaje': 'Notificación confirmada'})
        
    except DestinatarioNotificacion.DoesNotExist:
        return Response({
            'error': 'Notificación no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)

class ListaAvisosGenerales(generics.ListCreateAPIView):
    """
    Listar y crear avisos generales
    """
    queryset = AvisoGeneral.objects.filter(esta_activo=True)
    serializer_class = SerializadorAvisoGeneral
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = AvisoGeneral.objects.filter(esta_activo=True)
        
        # Filtrar por tipo si se especifica
        tipo = self.request.query_params.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_aviso=tipo)
        
        # Filtrar solo destacados si se especifica
        destacados = self.request.query_params.get('destacados')
        if destacados == 'true':
            queryset = queryset.filter(es_destacado=True)
        
        # Filtrar solo vigentes
        vigentes = self.request.query_params.get('vigentes')
        if vigentes == 'true':
            now = timezone.now()
            queryset = queryset.filter(
                fecha_inicio__lte=now
            ).filter(
                Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=now)
            )
        
        return queryset.order_by('-es_destacado', '-fecha_creacion')
    
    def perform_create(self, serializer):
        # Solo administradores pueden crear avisos
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Solo administradores pueden crear avisos")
        
        aviso = serializer.save(creado_por=self.request.user)
        
        # Crear notificación automática si se solicita
        if aviso.requiere_notificacion:
            try:
                # Obtener o crear categoría para avisos
                categoria, _ = CategoriaNotificacion.objects.get_or_create(
                    nombre='Avisos Generales',
                    defaults={
                        'descripcion': 'Avisos y comunicados generales',
                        'color': '#17a2b8',
                        'icono': 'bullhorn'
                    }
                )
                
                # Crear notificación
                notificacion = Notificacion.objects.create(
                    titulo=f"Nuevo aviso: {aviso.titulo}",
                    mensaje=aviso.contenido[:200] + "..." if len(aviso.contenido) > 200 else aviso.contenido,
                    categoria=categoria,
                    tipo_destinatario=aviso.dirigido_a,
                    edificios_objetivo=aviso.edificios_objetivo,
                    es_push=True,
                    es_urgente=aviso.tipo_aviso == 'urgente',
                    creado_por=self.request.user,
                    estado='enviada'
                )
                
                # Enviar la notificación
                NotificationService.enviar_notificacion(notificacion)
                
            except Exception as e:
                # Log del error pero no fallar la creación del aviso
                print(f"Error creando notificación para aviso {aviso.id}: {e}")

class DetalleAvisoGeneral(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar aviso general
    """
    queryset = AvisoGeneral.objects.all()
    serializer_class = SerializadorAvisoGeneral
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        """Incrementar visualizaciones al ver el aviso"""
        instance = self.get_object()
        
        # Incrementar contador de visualizaciones
        instance.visualizaciones += 1
        instance.save()
        
        # Registrar interacción de visualización
        InteraccionAviso.objects.get_or_create(
            aviso=instance,
            usuario=request.user,
            tipo_interaccion='visualizacion'
        )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def interactuar_aviso(request, aviso_id):
    """
    Registrar interacción con un aviso (like, dislike, compartir)
    """
    try:
        aviso = AvisoGeneral.objects.get(id=aviso_id)
    except AvisoGeneral.DoesNotExist:
        return Response({
            'error': 'Aviso no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    tipo_interaccion = request.data.get('tipo_interaccion')
    if tipo_interaccion not in ['like', 'dislike', 'compartir']:
        return Response({
            'error': 'Tipo de interacción inválido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Crear o actualizar interacción
    interaccion, created = InteraccionAviso.objects.get_or_create(
        aviso=aviso,
        usuario=request.user,
        tipo_interaccion=tipo_interaccion
    )
    
    if not created:
        # Si ya existía, actualizarla
        interaccion.fecha_interaccion = timezone.now()
        interaccion.save()
    
    # Actualizar contadores en el aviso
    if tipo_interaccion == 'like':
        aviso.likes = aviso.interacciones.filter(tipo_interaccion='like').count()
        aviso.save()
    
    return Response({
        'mensaje': f'Interacción {tipo_interaccion} registrada',
        'total_likes': aviso.likes
    })

class ConfiguracionNotificacionUsuario(generics.RetrieveUpdateAPIView):
    """
    Ver y actualizar configuración de notificaciones del usuario
    """
    serializer_class = SerializadorConfiguracionNotificacion
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        config, created = ConfiguracionNotificacion.objects.get_or_create(
            usuario=self.request.user
        )
        return config

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def actualizar_token_fcm(request):
    """
    Actualizar token FCM para notificaciones push
    """
    token = request.data.get('token')
    plataforma = request.data.get('plataforma', 'web')  # web, android, ios
    
    if not token:
        return Response({
            'error': 'Token requerido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    config, created = ConfiguracionNotificacion.objects.get_or_create(
        usuario=request.user
    )
    
    # Actualizar el token según la plataforma
    if plataforma == 'android':
        config.token_fcm_android = token
    elif plataforma == 'ios':
        config.token_fcm_ios = token
    else:
        config.token_fcm_web = token
    
    config.save()
    
    return Response({
        'mensaje': f'Token FCM actualizado para {plataforma}'
    })

class ListaPlantillas(generics.ListCreateAPIView):
    """
    Listar y crear plantillas de notificación
    """
    queryset = PlantillaNotificacion.objects.filter(esta_activa=True)
    serializer_class = SerializadorPlantillaNotificacion
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def renderizar_plantilla(request):
    """
    Renderizar una plantilla con variables específicas
    """
    serializador = SerializadorRenderizarPlantilla(data=request.data)
    if serializador.is_valid():
        plantilla_id = serializador.validated_data['plantilla_id']
        variables = serializador.validated_data['variables']
        
        plantilla = PlantillaNotificacion.objects.get(id=plantilla_id)
        resultado = plantilla.renderizar(**variables)
        
        # Incrementar contador de uso
        plantilla.uso_contador += 1
        plantilla.save()
        
        return Response({
            'titulo': resultado['titulo'],
            'mensaje': resultado['mensaje'],
            'variables_usadas': list(variables.keys())
        })
    
    return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def estadisticas_notificaciones(request):
    """
    Obtener estadísticas de notificaciones para el usuario
    """
    usuario = request.user
    
    # Estadísticas básicas
    mis_notificaciones = DestinatarioNotificacion.objects.filter(usuario=usuario)
    
    total_notificaciones = mis_notificaciones.count()
    total_leidas = mis_notificaciones.filter(fecha_lectura__isnull=False).count()
    total_no_leidas = total_notificaciones - total_leidas
    
    # Notificaciones por categoría (últimos 30 días)
    hace_30_dias = timezone.now() - timedelta(days=30)
    notif_por_categoria = mis_notificaciones.filter(
        fecha_envio__gte=hace_30_dias
    ).values(
        'notificacion__categoria__nombre',
        'notificacion__categoria__color'
    ).annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')
    
    # Notificaciones recientes (últimas 10)
    notif_recientes = mis_notificaciones.order_by('-fecha_envio')[:10]
    
    # Tasa de apertura promedio (si es administrador)
    tasa_apertura_promedio = 0
    if request.user.is_staff:
        notificaciones_enviadas = Notificacion.objects.filter(
            creado_por=usuario,
            total_enviados__gt=0
        )
        if notificaciones_enviadas.exists():
            tasa_apertura_promedio = notificaciones_enviadas.aggregate(
                promedio=Avg('total_leidos') * 100.0 / Avg('total_enviados')
            )['promedio'] or 0
    
    datos = {
        'total_notificaciones': total_notificaciones,
        'total_enviadas': total_notificaciones,  # Para el usuario son las mismas
        'total_pendientes': 0,  # Los usuarios no tienen pendientes
        'total_leidas': total_leidas,
        'total_no_leidas': total_no_leidas,
        'tasa_apertura_promedio': round(tasa_apertura_promedio, 2),
        'notificaciones_por_categoria': list(notif_por_categoria),
        'notificaciones_recientes': SerializadorNotificacionUsuario(notif_recientes, many=True).data
    }
    
    serializador = SerializadorEstadisticasNotificacion(data=datos)
    serializador.is_valid()
    
    return Response(serializador.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def notificacion_masiva(request):
    """
    Crear y enviar notificación masiva (solo administradores)
    """
    if not request.user.is_staff:
        return Response({
            'error': 'Solo administradores pueden enviar notificaciones masivas'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Crear la notificación
    serializador = SerializadorCrearNotificacion(data=request.data, context={'request': request})
    if serializador.is_valid():
        notificacion = serializador.save()
        
        # Enviar inmediatamente si se solicita
        if notificacion.enviar_inmediatamente:
            try:
                resultado = NotificationService.enviar_notificacion(notificacion)
                return Response({
                    'mensaje': 'Notificación creada y enviada exitosamente',
                    'notificacion_id': notificacion.id,
                    'destinatarios_procesados': resultado['total_destinatarios'],
                    'enviados_exitosos': resultado['enviados_exitosos']
                })
            except Exception as e:
                return Response({
                    'error': f'Notificación creada pero error al enviar: {str(e)}',
                    'notificacion_id': notificacion.id
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'mensaje': 'Notificación programada exitosamente',
                'notificacion_id': notificacion.id,
                'fecha_programada': notificacion.fecha_programada
            })
    
    return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)