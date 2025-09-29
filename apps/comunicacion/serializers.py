from rest_framework import serializers
from django.utils import timezone
from .models import (
    CategoriaNotificacion, Notificacion, DestinatarioNotificacion, 
    AvisoGeneral, InteraccionAviso, ConfiguracionNotificacion,
    PlantillaNotificacion
)
from apps.autenticacion.models import Usuario

class SerializadorCategoriaNotificacion(serializers.ModelSerializer):
    """
    Serializador para categorías de notificaciones
    """
    total_notificaciones = serializers.SerializerMethodField()
    
    class Meta:
        model = CategoriaNotificacion
        fields = [
            'id', 'nombre', 'descripcion', 'color', 'icono', 'prioridad',
            'esta_activa', 'fecha_creacion', 'total_notificaciones'
        ]
    
    def get_total_notificaciones(self, obj):
        return obj.notificaciones.count()

class SerializadorDestinatarioNotificacion(serializers.ModelSerializer):
    """
    Serializador para destinatarios de notificaciones
    """
    usuario_info = serializers.SerializerMethodField()
    
    class Meta:
        model = DestinatarioNotificacion
        fields = [
            'id', 'usuario', 'usuario_info', 'estado', 'fecha_envio',
            'fecha_entrega', 'fecha_lectura', 'fecha_confirmacion',
            'dispositivo_lectura', 'mensaje_error'
        ]
        read_only_fields = ['fecha_envio', 'fecha_entrega', 'fecha_lectura']
    
    def get_usuario_info(self, obj):
        return {
            'id': obj.usuario.id,
            'email': obj.usuario.email,
            'nombre_completo': obj.usuario.get_full_name(),
            'telefono': obj.usuario.telefono
        }

class SerializadorNotificacion(serializers.ModelSerializer):
    """
    Serializador principal para notificaciones
    """
    categoria_info = SerializadorCategoriaNotificacion(source='categoria', read_only=True)
    creado_por_nombre = serializers.CharField(source='creado_por.get_full_name', read_only=True)
    destinatarios = SerializadorDestinatarioNotificacion(many=True, read_only=True)
    tasa_apertura = serializers.ReadOnlyField()
    tasa_confirmacion = serializers.ReadOnlyField()
    
    class Meta:
        model = Notificacion
        fields = [
            'id', 'titulo', 'mensaje', 'categoria', 'categoria_info',
            'tipo_destinatario', 'edificios_objetivo', 'unidades_objetivo',
            'es_push', 'es_email', 'es_sms', 'es_urgente',
            'enviar_inmediatamente', 'fecha_programada', 'fecha_expiracion',
            'imagen', 'archivo_adjunto', 'requiere_confirmacion', 'metadatos',
            'estado', 'total_destinatarios', 'total_enviados', 'total_leidos',
            'total_confirmados', 'creado_por', 'creado_por_nombre',
            'fecha_creacion', 'fecha_envio', 'destinatarios', 'tasa_apertura',
            'tasa_confirmacion'
        ]
        read_only_fields = [
            'total_destinatarios', 'total_enviados', 'total_leidos',
            'total_confirmados', 'fecha_creacion', 'fecha_envio'
        ]
    
    def validate(self, data):
        """Validaciones personalizadas"""
        if data.get('fecha_programada') and data.get('enviar_inmediatamente'):
            raise serializers.ValidationError(
                "No se puede programar una fecha si se envía inmediatamente"
            )
        
        if data.get('fecha_programada') and data['fecha_programada'] <= timezone.now():
            raise serializers.ValidationError(
                "La fecha programada debe ser futura"
            )
        
        return data

class SerializadorCrearNotificacion(serializers.ModelSerializer):
    """
    Serializador para crear notificaciones
    """
    usuarios_especificos_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Notificacion
        fields = [
            'titulo', 'mensaje', 'categoria', 'tipo_destinatario',
            'usuarios_especificos_ids', 'edificios_objetivo', 'unidades_objetivo',
            'es_push', 'es_email', 'es_sms', 'es_urgente',
            'enviar_inmediatamente', 'fecha_programada', 'fecha_expiracion',
            'imagen', 'archivo_adjunto', 'requiere_confirmacion', 'metadatos'
        ]
    
    def create(self, validated_data):
        usuarios_especificos_ids = validated_data.pop('usuarios_especificos_ids', [])
        validated_data['creado_por'] = self.context['request'].user
        
        notificacion = Notificacion.objects.create(**validated_data)
        
        # Agregar usuarios específicos si se proporcionaron
        if usuarios_especificos_ids:
            usuarios = Usuario.objects.filter(id__in=usuarios_especificos_ids)
            for usuario in usuarios:
                DestinatarioNotificacion.objects.create(
                    notificacion=notificacion,
                    usuario=usuario
                )
        
        return notificacion

class SerializadorAvisoGeneral(serializers.ModelSerializer):
    """
    Serializador para avisos generales
    """
    creado_por_nombre = serializers.CharField(source='creado_por.get_full_name', read_only=True)
    esta_vigente = serializers.ReadOnlyField()
    tipo_aviso_display = serializers.CharField(source='get_tipo_aviso_display', read_only=True)
    
    class Meta:
        model = AvisoGeneral
        fields = [
            'id', 'titulo', 'contenido', 'tipo_aviso', 'tipo_aviso_display',
            'es_destacado', 'mostrar_en_inicio', 'requiere_notificacion',
            'fecha_inicio', 'fecha_fin', 'imagen_portada', 'archivo_adjunto',
            'dirigido_a', 'edificios_objetivo', 'visualizaciones', 'likes',
            'esta_activo', 'creado_por', 'creado_por_nombre', 'fecha_creacion',
            'esta_vigente'
        ]
        read_only_fields = ['visualizaciones', 'likes', 'fecha_creacion']

class SerializadorInteraccionAviso(serializers.ModelSerializer):
    """
    Serializador para interacciones con avisos
    """
    class Meta:
        model = InteraccionAviso
        fields = ['id', 'aviso', 'tipo_interaccion', 'fecha_interaccion']
        read_only_fields = ['fecha_interaccion']

class SerializadorConfiguracionNotificacion(serializers.ModelSerializer):
    """
    Serializador para configuración de notificaciones del usuario
    """
    class Meta:
        model = ConfiguracionNotificacion
        fields = [
            'id', 'recibir_push', 'recibir_email', 'recibir_sms',
            'notif_pagos', 'notif_mantenimiento', 'notif_seguridad',
            'notif_eventos', 'notif_avisos', 'notif_reservas',
            'horario_inicio', 'horario_fin', 'no_molestar_fines_semana',
            'token_fcm_android', 'token_fcm_ios', 'token_fcm_web'
        ]

class SerializadorPlantillaNotificacion(serializers.ModelSerializer):
    """
    Serializador para plantillas de notificación
    """
    categoria_default_info = SerializadorCategoriaNotificacion(source='categoria_default', read_only=True)
    
    class Meta:
        model = PlantillaNotificacion
        fields = [
            'id', 'nombre', 'descripcion', 'titulo_plantilla', 'mensaje_plantilla',
            'variables_disponibles', 'categoria_default', 'categoria_default_info',
            'es_push_default', 'es_email_default', 'es_sistema', 'esta_activa',
            'uso_contador', 'fecha_creacion'
        ]
        read_only_fields = ['uso_contador', 'fecha_creacion']

class SerializadorRenderizarPlantilla(serializers.Serializer):
    """
    Serializador para renderizar una plantilla de notificación con variables
    """
    plantilla_id = serializers.IntegerField()
    variables = serializers.DictField(required=False, default=dict)
    
    def validate_plantilla_id(self, value):
        try:
            PlantillaNotificacion.objects.get(id=value, esta_activa=True)
            return value
        except PlantillaNotificacion.DoesNotExist:
            raise serializers.ValidationError("Plantilla no encontrada")
    

class SerializadorNotificacionUsuario(serializers.ModelSerializer):

    categoria_info = SerializadorCategoriaNotificacion(source='notificacion.categoria', read_only=True)
    titulo = serializers.CharField(source='notificacion.titulo', read_only=True)
    mensaje = serializers.CharField(source='notificacion.mensaje', read_only=True)
    es_urgente = serializers.BooleanField(source='notificacion.es_urgente', read_only=True)
    imagen = serializers.ImageField(source='notificacion.imagen', read_only=True)
    requiere_confirmacion = serializers.BooleanField(source='notificacion.requiere_confirmacion', read_only=True)

    class Meta:
        model = DestinatarioNotificacion
        fields = [
            'id', 'titulo', 'mensaje', 'categoria_info', 'es_urgente',
            'imagen', 'estado', 'fecha_envio', 'fecha_lectura',
            'fecha_confirmacion', 'requiere_confirmacion'
        ]
class SerializadorEstadisticasNotificacion(serializers.Serializer):
    """
    Serializador para estadísticas de notificaciones
    """
    total_notificaciones = serializers.IntegerField()
    total_enviadas = serializers.IntegerField()
    total_pendientes = serializers.IntegerField()
    total_leidas = serializers.IntegerField()
    total_no_leidas = serializers.IntegerField()
    tasa_apertura_promedio = serializers.DecimalField(max_digits=5, decimal_places=2)
    notificaciones_por_categoria = serializers.ListField()
    notificaciones_recientes = SerializadorNotificacionUsuario(many=True)

class SerializadorMarcarLeida(serializers.Serializer):
    """
    Serializador para marcar notificación como leída
    """
    dispositivo = serializers.ChoiceField(
        choices=[('web', 'Web'), ('movil', 'Móvil'), ('email', 'Email')],
        default='web'
    )

class SerializadorTokenFCM(serializers.Serializer):
    """
    Serializador para actualizar tokens FCM
    """
    token = serializers.CharField(max_length=500)
    plataforma = serializers.ChoiceField(
        choices=[('web', 'Web'), ('android', 'Android'), ('ios', 'iOS')],
        default='web'
    )

class SerializadorFiltrosNotificacion(serializers.Serializer):
    """
    Serializador para filtros de notificaciones
    """
    estado = serializers.ChoiceField(
        choices=[('all', 'Todas')] + list(Notificacion.ESTADOS),
        default='all',
        required=False
    )
    categoria = serializers.IntegerField(required=False)
    urgente = serializers.BooleanField(required=False)
    tipo_destinatario = serializers.ChoiceField(
        choices=Notificacion.TIPOS_DESTINATARIO,
        required=False
    )
    fecha_desde = serializers.DateTimeField(required=False)
    fecha_hasta = serializers.DateTimeField(required=False)

class SerializadorEnvioNotificacion(serializers.Serializer):
    """
    Serializador para respuesta del envío de notificaciones
    """
    mensaje = serializers.CharField()
    destinatarios_procesados = serializers.IntegerField()
    enviados_exitosos = serializers.IntegerField()
    errores = serializers.ListField(child=serializers.CharField(), required=False)

class SerializadorUsuarioBasico(serializers.ModelSerializer):
    """
    Serializador básico para información de usuario en notificaciones
    """
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre_completo', 'telefono']
    
    def get_nombre_completo(self, obj):
        return obj.get_full_name()

class SerializadorCrearAviso(serializers.ModelSerializer):
    """
    Serializador específico para crear avisos generales
    """
    class Meta:
        model = AvisoGeneral
        fields = [
            'titulo', 'contenido', 'tipo_aviso', 'es_destacado',
            'mostrar_en_inicio', 'requiere_notificacion', 'fecha_inicio',
            'fecha_fin', 'imagen_portada', 'archivo_adjunto', 'dirigido_a',
            'edificios_objetivo'
        ]
    
    def validate(self, data):
        """Validaciones personalizadas para avisos"""
        if data.get('fecha_fin') and data['fecha_fin'] <= data['fecha_inicio']:
            raise serializers.ValidationError(
                "La fecha de fin debe ser posterior a la fecha de inicio"
            )
        return data

class SerializadorResumenNotificacion(serializers.ModelSerializer):
    """
    Serializador resumido para listados de notificaciones
    """
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    categoria_color = serializers.CharField(source='categoria.color', read_only=True)
    creado_por_nombre = serializers.CharField(source='creado_por.get_full_name', read_only=True)
    
    class Meta:
        model = Notificacion
        fields = [
            'id', 'titulo', 'categoria_nombre', 'categoria_color',
            'tipo_destinatario', 'es_urgente', 'estado',
            'total_destinatarios', 'total_leidos', 'tasa_apertura',
            'creado_por_nombre', 'fecha_creacion', 'fecha_envio'
        ]

class SerializadorValidacionMasiva(serializers.Serializer):
    """
    Serializador para validar datos de notificación masiva
    """
    titulo = serializers.CharField(max_length=200)
    mensaje = serializers.CharField()
    categoria_id = serializers.IntegerField()
    tipo_destinatario = serializers.ChoiceField(choices=Notificacion.TIPOS_DESTINATARIO)
    usuarios_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
    edificios = serializers.ListField(
        child=serializers.CharField(max_length=10),
        required=False,
        allow_empty=True
    )
    unidades_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
    canales = serializers.ListField(
        child=serializers.ChoiceField(choices=[('push', 'Push'), ('email', 'Email'), ('sms', 'SMS')]),
        required=False,
        default=['push']
    )
    es_urgente = serializers.BooleanField(default=False)
    programar = serializers.BooleanField(default=False)
    fecha_programada = serializers.DateTimeField(required=False)
    
    def validate(self, data):
        # Validar que existe la categoría
        try:
            CategoriaNotificacion.objects.get(id=data['categoria_id'], esta_activa=True)
        except CategoriaNotificacion.DoesNotExist:
            raise serializers.ValidationError("Categoría no válida")
        
        # Validar programación
        if data.get('programar') and not data.get('fecha_programada'):
            raise serializers.ValidationError(
                "Debe especificar fecha_programada si programar es True"
            )
        
        if data.get('fecha_programada') and data['fecha_programada'] <= timezone.now():
            raise serializers.ValidationError(
                "La fecha programada debe ser futura"
            )
        
        # Validar destinatarios específicos
        tipo_dest = data['tipo_destinatario']
        if tipo_dest == 'usuarios' and not data.get('usuarios_ids'):
            raise serializers.ValidationError(
                "Debe especificar usuarios_ids para tipo 'usuarios'"
            )
        
        if tipo_dest == 'edificio' and not data.get('edificios'):
            raise serializers.ValidationError(
                "Debe especificar edificios para tipo 'edificio'"
            )
        
        if tipo_dest == 'unidades' and not data.get('unidades_ids'):
            raise serializers.ValidationError(
                "Debe especificar unidades_ids para tipo 'unidades'"
            )
        
        return data

