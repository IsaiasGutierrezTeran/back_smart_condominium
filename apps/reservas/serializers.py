from rest_framework import serializers
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
from .models import (
    TipoAreaComun, AreaComun, Reserva, ImagenAreaComun, 
    ServicioAdicional, ReservaServicio, DisponibilidadEspecial
)
from apps.autenticacion.models import Usuario
from apps.finanzas.models import UnidadHabitacional

class SerializadorTipoAreaComun(serializers.ModelSerializer):
    """
    Serializador para tipos de áreas comunes
    """
    total_areas = serializers.SerializerMethodField()
    
    class Meta:
        model = TipoAreaComun
        fields = [
            'id', 'nombre', 'descripcion', 'icono', 'color', 'requiere_deposito',
            'permite_equipos_externos', 'esta_activo', 'orden', 'total_areas'
        ]
    
    def get_total_areas(self, obj):
        return obj.areas.filter(permite_reservas=True, estado='disponible').count()

class SerializadorImagenAreaComun(serializers.ModelSerializer):
    """
    Serializador para imágenes de áreas comunes
    """
    class Meta:
        model = ImagenAreaComun
        fields = ['id', 'imagen', 'titulo', 'descripcion', 'es_portada', 'orden']

class SerializadorServicioAdicional(serializers.ModelSerializer):
    """
    Serializador para servicios adicionales
    """
    class Meta:
        model = ServicioAdicional
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'unidad',
            'requiere_anticipacion', 'esta_activo'
        ]

class SerializadorAreaComun(serializers.ModelSerializer):
    """
    Serializador para áreas comunes
    """
    tipo_area_info = SerializadorTipoAreaComun(source='tipo_area', read_only=True)
    imagenes = SerializadorImagenAreaComun(many=True, read_only=True)
    servicios_disponibles = SerializadorServicioAdicional(many=True, read_only=True)
    esta_disponible = serializers.ReadOnlyField()
    tarifa_actual = serializers.ReadOnlyField()
    
    class Meta:
        model = AreaComun
        fields = [
            'id', 'nombre', 'descripcion', 'tipo_area', 'tipo_area_info',
            'capacidad_maxima', 'area_m2', 'ubicacion', 'permite_reservas',
            'tiempo_minimo_reserva', 'tiempo_maximo_reserva', 'anticipacion_minima',
            'anticipacion_maxima', 'horario_funcionamiento', 'tarifa_por_hora',
            'tarifa_fin_semana', 'deposito_garantia', 'requiere_autorizacion',
            'permite_decoracion', 'permite_musica', 'permite_comida_externa',
            'incluye_mobiliario', 'incluye_audio', 'incluye_iluminacion',
            'reglas_uso', 'equipamiento_incluido', 'restricciones_especiales',
            'estado', 'imagen_principal', 'total_reservas', 'rating_promedio',
            'imagenes', 'servicios_disponibles', 'esta_disponible', 'tarifa_actual'
        ]

class SerializadorAreaComunSimple(serializers.ModelSerializer):
    """
    Serializador simplificado para áreas comunes (para listas)
    """
    tipo_area_nombre = serializers.CharField(source='tipo_area.nombre', read_only=True)
    tipo_area_icono = serializers.CharField(source='tipo_area.icono', read_only=True)
    tipo_area_color = serializers.CharField(source='tipo_area.color', read_only=True)
    esta_disponible = serializers.ReadOnlyField()
    tarifa_actual = serializers.ReadOnlyField()
    
    class Meta:
        model = AreaComun
        fields = [
            'id', 'nombre', 'descripcion', 'tipo_area_nombre', 'tipo_area_icono',
            'tipo_area_color', 'capacidad_maxima', 'ubicacion', 'tarifa_por_hora',
            'tarifa_fin_semana', 'imagen_principal', 'rating_promedio',
            'esta_disponible', 'tarifa_actual', 'estado'
        ]

class SerializadorReservaServicio(serializers.ModelSerializer):
    """
    Serializador para servicios de reserva
    """
    servicio_info = SerializadorServicioAdicional(source='servicio', read_only=True)
    
    class Meta:
        model = ReservaServicio
        fields = [
            'id', 'servicio', 'servicio_info', 'cantidad', 'precio_unitario',
            'precio_total', 'observaciones'
        ]
        read_only_fields = ['precio_total']

class SerializadorReserva(serializers.ModelSerializer):
    """
    Serializador principal para reservas
    """
    area_comun_info = SerializadorAreaComunSimple(source='area_comun', read_only=True)
    usuario_info = serializers.SerializerMethodField()
    unidad_info = serializers.SerializerMethodField()
    servicios_contratados = SerializadorReservaServicio(many=True, read_only=True)
    puede_ser_cancelada = serializers.ReadOnlyField()
    tipo_evento_display = serializers.CharField(source='get_tipo_evento_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Reserva
        fields = [
            'id', 'area_comun', 'area_comun_info', 'usuario', 'usuario_info',
            'unidad', 'unidad_info', 'fecha_reserva', 'hora_inicio', 'hora_fin',
            'duracion_minutos', 'tipo_evento', 'tipo_evento_display', 'nombre_evento',
            'descripcion', 'numero_invitados', 'requiere_decoracion', 'requiere_audio',
            'requiere_iluminacion', 'requiere_seguridad', 'requiere_limpieza_extra',
            'telefono_contacto', 'email_contacto', 'contacto_emergencia',
            'costo_base', 'costo_servicios_adicionales', 'deposito_garantia',
            'costo_total', 'estado', 'estado_display', 'requiere_aprobacion',
            'aprobado_por', 'fecha_aprobacion', 'observaciones_usuario',
            'observaciones_admin', 'motivo_cancelacion', 'calificacion',
            'comentario_calificacion', 'codigo_reserva', 'fecha_creacion',
            'servicios_contratados', 'puede_ser_cancelada'
        ]
        read_only_fields = [
            'duracion_minutos', 'costo_base', 'costo_servicios_adicionales',
            'deposito_garantia', 'costo_total', 'codigo_reserva', 'fecha_creacion'
        ]
    
    def get_usuario_info(self, obj):
        return {
            'id': obj.usuario.id,
            'email': obj.usuario.email,
            'nombre_completo': obj.usuario.get_full_name(),
            'telefono': obj.usuario.telefono
        }
    
    def get_unidad_info(self, obj):
        return {
            'id': obj.unidad.id,
            'numero_unidad': obj.unidad.numero_unidad,
            'edificio': obj.unidad.edificio
        }

class SerializadorCrearReserva(serializers.ModelSerializer):
    """
    Serializador para crear nuevas reservas
    """
    servicios_adicionales = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text="Lista de servicios: [{'servicio_id': 1, 'cantidad': 2}]"
    )
    
    class Meta:
        model = Reserva
        fields = [
            'area_comun', 'fecha_reserva', 'hora_inicio', 'hora_fin',
            'tipo_evento', 'nombre_evento', 'descripcion', 'numero_invitados',
            'requiere_decoracion', 'requiere_audio', 'requiere_iluminacion',
            'requiere_seguridad', 'requiere_limpieza_extra', 'telefono_contacto',
            'email_contacto', 'contacto_emergencia', 'observaciones_usuario',
            'servicios_adicionales'
        ]
    
    def validate(self, data):
        """Validaciones personalizadas"""
        area_comun = data['area_comun']
        fecha_reserva = data['fecha_reserva']
        hora_inicio = data['hora_inicio']
        hora_fin = data['hora_fin']
        
        # Validar que el área esté disponible
        if not area_comun.esta_disponible:
            raise serializers.ValidationError("El área seleccionada no está disponible")
        
        # Validar fecha futura
        if fecha_reserva <= timezone.now().date():
            raise serializers.ValidationError("La fecha de reserva debe ser futura")
        
        # Validar horarios
        fecha_hora_inicio = datetime.combine(fecha_reserva, hora_inicio)
        fecha_hora_inicio = timezone.make_aware(fecha_hora_inicio)
        
        if not area_comun.esta_disponible_en_horario(fecha_hora_inicio):
            raise serializers.ValidationError(
                "El área no está disponible en el horario seleccionado"
            )
        
        # Validar solapamientos con otras reservas
        reservas_existentes = Reserva.objects.filter(
            area_comun=area_comun,
            fecha_reserva=fecha_reserva,
            estado__in=['pendiente', 'confirmada', 'en_uso']
        ).exclude(
            # Excluir la reserva actual si es una actualización
            id=self.instance.id if self.instance else None
        )
        
        for reserva in reservas_existentes:
            if not (hora_fin <= reserva.hora_inicio or hora_inicio >= reserva.hora_fin):
                raise serializers.ValidationError(
                    f"Ya existe una reserva en este horario: {reserva.codigo_reserva}"
                )
        
        return data
    
    def create(self, validated_data):
        servicios_adicionales = validated_data.pop('servicios_adicionales', [])
        
        # Obtener usuario y unidad
        usuario = self.context['request'].user
        
        # Buscar unidad del usuario
        unidad = UnidadHabitacional.objects.filter(
            models.Q(propietario=usuario) | models.Q(inquilino=usuario)
        ).first()
        
        if not unidad:
            raise serializers.ValidationError(
                "No se encontró una unidad asociada al usuario"
            )
        
        validated_data['usuario'] = usuario
        validated_data['unidad'] = unidad
        
        # Verificar si requiere aprobación
        area_comun = validated_data['area_comun']
        if area_comun.requiere_autorizacion:
            validated_data['requiere_aprobacion'] = True
            validated_data['estado'] = 'pendiente'
        else:
            validated_data['estado'] = 'confirmada'
        
        # Crear la reserva
        reserva = Reserva.objects.create(**validated_data)
        
        # Agregar servicios adicionales
        for servicio_data in servicios_adicionales:
            try:
                servicio = ServicioAdicional.objects.get(
                    id=servicio_data['servicio_id'],
                    esta_activo=True
                )
                ReservaServicio.objects.create(
                    reserva=reserva,
                    servicio=servicio,
                    cantidad=servicio_data.get('cantidad', 1),
                    precio_unitario=servicio.precio
                )
            except ServicioAdicional.DoesNotExist:
                continue
        
        return reserva

class SerializadorDisponibilidad(serializers.Serializer):
    """
    Serializador para consultar disponibilidad
    """
    area_comun_id = serializers.IntegerField()
    fecha = serializers.DateField()
    
    def validate_area_comun_id(self, value):
        try:
            area = AreaComun.objects.get(id=value, permite_reservas=True)
            return value
        except AreaComun.DoesNotExist:
            raise serializers.ValidationError("Área común no encontrada o no permite reservas")
    
    def validate_fecha(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("La fecha debe ser futura")
        return value

class SerializadorHorarioDisponible(serializers.Serializer):
    """
    Serializador para horarios disponibles
    """
    hora_inicio = serializers.TimeField()
    hora_fin = serializers.TimeField()
    disponible = serializers.BooleanField()
    motivo = serializers.CharField(required=False)

class SerializadorDisponibilidadEspecial(serializers.ModelSerializer):
    """
    Serializador para disponibilidades especiales
    """
    class Meta:
        model = DisponibilidadEspecial
        fields = [
            'id', 'area_comun', 'tipo', 'titulo', 'descripcion',
            'fecha_inicio', 'fecha_fin', 'esta_disponible',
            'tarifa_especial', 'fecha_creacion'
        ]

class SerializadorEstadisticasReservas(serializers.Serializer):
    """
    Serializador para estadísticas de reservas
    """
    total_reservas = serializers.IntegerField()
    reservas_confirmadas = serializers.IntegerField()
    reservas_pendientes = serializers.IntegerField()
    reservas_canceladas = serializers.IntegerField()
    reservas_completadas = serializers.IntegerField()
    tasa_ocupacion = serializers.DecimalField(max_digits=5, decimal_places=2)
    ingresos_mes_actual = serializers.DecimalField(max_digits=10, decimal_places=2)
    area_mas_popular = serializers.CharField()
    horario_mas_solicitado = serializers.CharField()
    reservas_por_tipo_evento = serializers.ListField()
    reservas_recientes = SerializadorReserva(many=True)
