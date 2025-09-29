from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    TipoVisitante, RegistroVisitante, AccesoVehiculo, RegistroAcceso,
    IncidenteSeguridad, ConfiguracionIA, AnalisisPredictivoMorosidad
)
from apps.finanzas.models import UnidadHabitacional
from apps.autenticacion.serializers import UsuarioSerializer

User = get_user_model()

class TipoVisitanteSerializer(serializers.ModelSerializer):
    """Serializer para tipos de visitantes"""
    
    class Meta:
        model = TipoVisitante
        fields = [
            'id', 'nombre', 'descripcion', 'requiere_autorizacion',
            'tiempo_maximo_visita', 'color', 'icono', 'esta_activo',
            'fecha_creacion'
        ]
        read_only_fields = ['id', 'fecha_creacion']

class RegistroVisitanteSerializer(serializers.ModelSerializer):
    """Serializer para registro de visitantes con IA"""
    
    # Campos relacionados
    tipo_visitante_info = TipoVisitanteSerializer(source='tipo_visitante', read_only=True)
    unidad_destino_info = serializers.StringRelatedField(source='unidad_destino', read_only=True)
    autorizado_por_info = UsuarioSerializer(source='autorizado_por', read_only=True)
    registrado_por_info = UsuarioSerializer(source='registrado_por', read_only=True)
    
    # Campos calculados
    nombre_completo = serializers.ReadOnlyField()
    esta_en_visita = serializers.ReadOnlyField()
    
    # URLs de imágenes
    foto_ingreso_url = serializers.SerializerMethodField()
    foto_salida_url = serializers.SerializerMethodField()
    
    class Meta:
        model = RegistroVisitante
        fields = [
            'id', 'nombres', 'apellidos', 'nombre_completo', 'documento_identidad',
            'telefono', 'tipo_visitante', 'tipo_visitante_info', 'unidad_destino',
            'unidad_destino_info', 'motivo_visita', 'autorizado_por',
            'autorizado_por_info', 'estado', 'foto_ingreso', 'foto_ingreso_url',
            'foto_salida', 'foto_salida_url', 'metodo_identificacion',
            'datos_faciales_json', 'confianza_reconocimiento',
            'fecha_autorizacion', 'fecha_ingreso', 'fecha_salida',
            'tiempo_estimado_visita', 'registrado_por', 'registrado_por_info',
            'observaciones', 'codigo_qr', 'esta_en_visita', 'fecha_creacion',
            'fecha_actualizacion'
        ]
        read_only_fields = [
            'id', 'nombre_completo', 'esta_en_visita', 'codigo_qr',
            'fecha_creacion', 'fecha_actualizacion'
        ]
    
    def get_foto_ingreso_url(self, obj):
        if obj.foto_ingreso:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_ingreso.url)
        return None
    
    def get_foto_salida_url(self, obj):
        if obj.foto_salida:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_salida.url)
        return None

class AccesoVehiculoSerializer(serializers.ModelSerializer):
    """Serializer para acceso vehicular con OCR"""
    
    # Campos relacionados
    propietario_info = UsuarioSerializer(source='propietario', read_only=True)
    unidad_asignada_info = serializers.StringRelatedField(source='unidad_asignada', read_only=True)
    registrado_por_info = UsuarioSerializer(source='registrado_por', read_only=True)
    
    # URLs de imágenes
    foto_vehiculo_url = serializers.SerializerMethodField()
    foto_placa_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AccesoVehiculo
        fields = [
            'id', 'placa_vehiculo', 'tipo_vehiculo', 'marca', 'modelo',
            'color', 'año', 'propietario', 'propietario_info',
            'unidad_asignada', 'unidad_asignada_info', 'foto_vehiculo',
            'foto_vehiculo_url', 'foto_placa', 'foto_placa_url',
            'datos_ocr_json', 'confianza_ocr', 'estado_acceso',
            'es_vehiculo_residente', 'acceso_temporal_hasta',
            'numero_estacionamiento', 'observaciones', 'registrado_por',
            'registrado_por_info', 'esta_activo', 'fecha_creacion',
            'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def get_foto_vehiculo_url(self, obj):
        if obj.foto_vehiculo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_vehiculo.url)
        return None
    
    def get_foto_placa_url(self, obj):
        if obj.foto_placa:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_placa.url)
        return None

class RegistroAccesoSerializer(serializers.ModelSerializer):
    """Serializer para registro de accesos"""
    
    # Campos relacionados
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)
    visitante_info = serializers.StringRelatedField(source='visitante', read_only=True)
    vehiculo_info = serializers.StringRelatedField(source='vehiculo', read_only=True)
    
    # URL de foto
    foto_acceso_url = serializers.SerializerMethodField()
    
    class Meta:
        model = RegistroAcceso
        fields = [
            'id', 'tipo_acceso', 'metodo_acceso', 'usuario', 'usuario_info',
            'visitante', 'visitante_info', 'vehiculo', 'vehiculo_info',
            'fecha_hora', 'ubicacion_acceso', 'foto_acceso', 'foto_acceso_url',
            'datos_biometricos', 'confianza_identificacion', 'acceso_autorizado',
            'requiere_atencion', 'observaciones', 'dispositivo_origen',
            'ip_address'
        ]
        read_only_fields = ['id', 'fecha_hora']
    
    def get_foto_acceso_url(self, obj):
        if obj.foto_acceso:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_acceso.url)
        return None

class IncidenteSeguridadSerializer(serializers.ModelSerializer):
    """Serializer para incidentes de seguridad"""
    
    # Campos relacionados
    usuario_involucrado_info = UsuarioSerializer(source='usuario_involucrado', read_only=True)
    visitante_involucrado_info = serializers.StringRelatedField(source='visitante_involucrado', read_only=True)
    vehiculo_involucrado_info = serializers.StringRelatedField(source='vehiculo_involucrado', read_only=True)
    reportado_por_info = UsuarioSerializer(source='reportado_por', read_only=True)
    asignado_a_info = UsuarioSerializer(source='asignado_a', read_only=True)
    
    # URLs de archivos multimedia
    foto_incidente_url = serializers.SerializerMethodField()
    video_incidente_url = serializers.SerializerMethodField()
    
    class Meta:
        model = IncidenteSeguridad
        fields = [
            'id', 'codigo_incidente', 'tipo_incidente', 'nivel_gravedad',
            'titulo', 'descripcion', 'ubicacion', 'coordenadas_gps',
            'detectado_por_ia', 'algoritmo_deteccion', 'confianza_deteccion',
            'foto_incidente', 'foto_incidente_url', 'video_incidente',
            'video_incidente_url', 'usuario_involucrado', 'usuario_involucrado_info',
            'visitante_involucrado', 'visitante_involucrado_info',
            'vehiculo_involucrado', 'vehiculo_involucrado_info', 'estado',
            'reportado_por', 'reportado_por_info', 'asignado_a', 'asignado_a_info',
            'fecha_incidente', 'fecha_reporte', 'fecha_resolucion',
            'acciones_tomadas', 'notas_seguimiento', 'datos_analisis_ia'
        ]
        read_only_fields = [
            'id', 'codigo_incidente', 'fecha_reporte'
        ]
    
    def get_foto_incidente_url(self, obj):
        if obj.foto_incidente:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_incidente.url)
        return None
    
    def get_video_incidente_url(self, obj):
        if obj.video_incidente:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_incidente.url)
        return None

class ConfiguracionIASerializer(serializers.ModelSerializer):
    """Serializer para configuración de IA"""
    
    # Campos relacionados
    creado_por_info = UsuarioSerializer(source='creado_por', read_only=True)
    
    class Meta:
        model = ConfiguracionIA
        fields = [
            'id', 'nombre', 'tipo_algoritmo', 'descripcion', 'modelo_ia',
            'parametros_configuracion', 'umbral_confianza', 'esta_activo',
            'version_modelo', 'fecha_ultima_actualizacion', 'precision_promedio',
            'recall_promedio', 'tiempo_procesamiento_ms', 'generar_alertas',
            'nivel_alerta_minimo', 'creado_por', 'creado_por_info',
            'fecha_creacion'
        ]
        read_only_fields = [
            'id', 'fecha_ultima_actualizacion', 'fecha_creacion'
        ]

class AnalisisPredictivoMorosidadSerializer(serializers.ModelSerializer):
    """Serializer para análisis predictivo de morosidad"""
    
    # Campos relacionados
    unidad_info = serializers.StringRelatedField(source='unidad', read_only=True)
    usuario_analizado_info = UsuarioSerializer(source='usuario_analizado', read_only=True)
    generado_por_info = UsuarioSerializer(source='generado_por', read_only=True)
    
    class Meta:
        model = AnalisisPredictivoMorosidad
        fields = [
            'id', 'unidad', 'unidad_info', 'usuario_analizado',
            'usuario_analizado_info', 'probabilidad_morosidad', 'nivel_riesgo',
            'factores_riesgo', 'historial_pagos_analizado', 'recomendaciones',
            'acciones_sugeridas', 'modelo_utilizado', 'version_modelo',
            'confianza_prediccion', 'fecha_analisis', 'valido_hasta',
            'fue_preciso', 'generado_por', 'generado_por_info'
        ]
        read_only_fields = ['id', 'fecha_analisis']

# Serializers simplificados para listas
class RegistroVisitanteListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de visitantes"""
    
    nombre_completo = serializers.ReadOnlyField()
    tipo_visitante_nombre = serializers.CharField(source='tipo_visitante.nombre', read_only=True)
    unidad_destino_numero = serializers.CharField(source='unidad_destino.numero_unidad', read_only=True)
    
    class Meta:
        model = RegistroVisitante
        fields = [
            'id', 'nombre_completo', 'documento_identidad', 'tipo_visitante_nombre',
            'unidad_destino_numero', 'estado', 'fecha_ingreso', 'motivo_visita'
        ]

class AccesoVehiculoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de vehículos"""
    
    propietario_nombre = serializers.CharField(source='propietario.get_full_name', read_only=True)
    unidad_numero = serializers.CharField(source='unidad_asignada.numero_unidad', read_only=True)
    
    class Meta:
        model = AccesoVehiculo
        fields = [
            'id', 'placa_vehiculo', 'tipo_vehiculo', 'marca', 'modelo',
            'propietario_nombre', 'unidad_numero', 'estado_acceso',
            'es_vehiculo_residente'
        ]

class IncidenteSeguridadListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de incidentes"""
    
    reportado_por_nombre = serializers.CharField(source='reportado_por.get_full_name', read_only=True)
    
    class Meta:
        model = IncidenteSeguridad
        fields = [
            'id', 'codigo_incidente', 'titulo', 'tipo_incidente',
            'nivel_gravedad', 'estado', 'fecha_incidente', 'reportado_por_nombre',
            'detectado_por_ia'
        ]

# Serializers para operaciones específicas de IA
class ReconocimientoFacialSerializer(serializers.Serializer):
    """Serializer para operaciones de reconocimiento facial"""
    
    imagen = serializers.ImageField(required=True)
    confianza_minima = serializers.DecimalField(
        max_digits=5, decimal_places=2, default=80.00, required=False
    )
    incluir_datos_biometricos = serializers.BooleanField(default=True, required=False)
    
    def validate_imagen(self, value):
        """Validar que la imagen sea válida para reconocimiento facial"""
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError("La imagen no puede ser mayor a 10MB")
        
        valid_extensions = ['jpg', 'jpeg', 'png']
        ext = value.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                f"Formato de imagen no válido. Use: {', '.join(valid_extensions)}"
            )
        
        return value

class OCRPlacaSerializer(serializers.Serializer):
    """Serializer para OCR de placas vehiculares"""
    
    imagen = serializers.ImageField(required=True)
    confianza_minima = serializers.DecimalField(
        max_digits=5, decimal_places=2, default=75.00, required=False
    )
    pais_formato = serializers.CharField(max_length=10, default='BO', required=False)
    
    def validate_imagen(self, value):
        """Validar que la imagen sea válida para OCR"""
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError("La imagen no puede ser mayor a 5MB")
        
        return value

class DeteccionAnomaliaSerializer(serializers.Serializer):
    """Serializer para detección de anomalías"""
    
    imagen_o_video = serializers.FileField(required=True)
    tipo_analisis = serializers.ChoiceField(
        choices=[
            ('movimiento', 'Análisis de Movimiento'),
            ('presencia', 'Detección de Presencia'),
            ('comportamiento', 'Análisis de Comportamiento'),
            ('objeto', 'Detección de Objetos')
        ],
        default='movimiento'
    )
    zona_analisis = serializers.JSONField(required=False, help_text="Coordenadas de la zona a analizar")
    sensibilidad = serializers.DecimalField(
        max_digits=5, decimal_places=2, default=70.00, 
        min_value=10.00, max_value=100.00, required=False
    )

class AnalisisMorosidadSerializer(serializers.Serializer):
    """Serializer para solicitar análisis de morosidad"""
    
    unidad_id = serializers.IntegerField(required=True)
    incluir_factores_externos = serializers.BooleanField(default=True, required=False)
    modelo_version = serializers.CharField(max_length=20, required=False)
    
    def validate_unidad_id(self, value):
        """Validar que la unidad existe"""
        try:
            UnidadHabitacional.objects.get(id=value)
        except UnidadHabitacional.DoesNotExist:
            raise serializers.ValidationError("La unidad especificada no existe")
        
        return value
