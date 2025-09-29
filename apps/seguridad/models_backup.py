from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from apps.autenticacion.models import Usuario
from apps.finanzas.models import UnidadHabitacional
from decimal import Decimal
import uuid
import os

def upload_to_seguridad(instance, filename):
    """Genera ruta de upload para archivos de seguridad"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('seguridad', instance.__class__.__name__.lower(), filename)

class TipoVisitante(models.Model):
    """
    Tipos de visitantes para clasificación
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    requiere_autorizacion = models.BooleanField(default=True, verbose_name="Requiere Autorización")
    tiempo_maximo_visita = models.PositiveIntegerField(
        default=480,  # 8 horas en minutos
        help_text="Tiempo máximo de visita en minutos",
        verbose_name="Tiempo Máximo (minutos)"
    )
    color = models.CharField(
        max_length=7,
        default="#007bff",
        help_text="Color hexadecimal para identificación visual",
        verbose_name="Color"
    )
    icono = models.CharField(
        max_length=50,
        default="person",
        help_text="Icono para representar el tipo",
        verbose_name="Icono"
    )
    esta_activo = models.BooleanField(default=True, verbose_name="Está Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tipo de Visitante"
        verbose_name_plural = "Tipos de Visitantes"
        db_table = "tipos_visitantes"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class RegistroVisitante(models.Model):
    """
    Registro de visitantes con IA y reconocimiento facial
    """
    ESTADOS_VISITA = (
        ('pendiente', 'Pendiente de Autorización'),
        ('autorizado', 'Autorizado'),
        ('en_visita', 'En Visita'),
        ('finalizado', 'Visita Finalizada'),
        ('rechazado', 'Rechazado'),
        ('vencido', 'Tiempo Vencido'),
    )
    
    METODOS_IDENTIFICACION = (
        ('manual', 'Registro Manual'),
        ('facial', 'Reconocimiento Facial'),
        ('qr', 'Código QR'),
        ('documento', 'Documento de Identidad'),
        ('biometrico', 'Datos Biométricos'),
    )
    
    # Información básica del visitante
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    documento_identidad = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(r'^\d{7,12}$', 'Documento debe contener 7-12 dígitos')],
        verbose_name="Documento de Identidad"
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?[\d\-\(\)\s]+$', 'Formato de teléfono inválido')],
        verbose_name="Teléfono"
    )
    
    # Información de la visita
    tipo_visitante = models.ForeignKey(
        TipoVisitante,
        on_delete=models.CASCADE,
        related_name='visitas',
        verbose_name="Tipo de Visitante"
    )
    unidad_destino = models.ForeignKey(
        UnidadHabitacional,
        on_delete=models.CASCADE,
        related_name='visitas_recibidas',
        verbose_name="Unidad de Destino"
    )
    motivo_visita = models.CharField(max_length=200, verbose_name="Motivo de la Visita")
    
    # Autorización
    autorizado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='visitas_autorizadas',
        verbose_name="Autorizado por"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_VISITA,
        default='pendiente',
        verbose_name="Estado"
    )
    
    # Datos de IA y reconocimiento facial
    foto_ingreso = models.ImageField(
        upload_to=upload_to_seguridad,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="Foto de Ingreso"
    )
    foto_salida = models.ImageField(
        upload_to=upload_to_seguridad,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="Foto de Salida"
    )
    metodo_identificacion = models.CharField(
        max_length=20,
        choices=METODOS_IDENTIFICACION,
        default='manual',
        verbose_name="Método de Identificación"
    )
    
    # Datos biométricos y de IA
    datos_faciales_json = models.JSONField(
        default=dict,
        blank=True,
        help_text="Datos de reconocimiento facial en formato JSON",
        verbose_name="Datos Faciales"
    )
    confianza_reconocimiento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Porcentaje de confianza del reconocimiento facial",
        verbose_name="Confianza de Reconocimiento (%)"
    )
    
    # Control de tiempo
    fecha_autorizacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Autorización")
    fecha_ingreso = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Ingreso")
    fecha_salida = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Salida")
    tiempo_estimado_visita = models.PositiveIntegerField(
        default=120,  # 2 horas
        help_text="Tiempo estimado de visita en minutos",
        verbose_name="Tiempo Estimado (minutos)"
    )
    
    # Personal de seguridad
    registrado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='visitas_registradas',
        verbose_name="Registrado por"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    codigo_qr = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        help_text="Código QR único para el visitante",
        verbose_name="Código QR"
    )
    
    class Meta:
        verbose_name = "Registro de Visitante"
        verbose_name_plural = "Registros de Visitantes"
        db_table = "registros_visitantes"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_ingreso']),
            models.Index(fields=['documento_identidad']),
        ]
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.unidad_destino}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def esta_en_visita(self):
        return self.estado == 'en_visita'
    
    def save(self, *args, **kwargs):
        if not self.codigo_qr:
            self.codigo_qr = f"VIS-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class AccesoVehiculo(models.Model):
    """
    Control de acceso vehicular con reconocimiento de placas (OCR + IA)
    """
    TIPOS_VEHICULO = (
        ('auto', 'Automóvil'),
        ('moto', 'Motocicleta'),
        ('camioneta', 'Camioneta'),
        ('van', 'Van'),
        ('camion', 'Camión'),
        ('bicicleta', 'Bicicleta'),
        ('otro', 'Otro'),
    )
    
    ESTADOS_ACCESO = (
        ('autorizado', 'Autorizado'),
        ('denegado', 'Denegado'),
        ('temporal', 'Acceso Temporal'),
        ('visitante', 'Vehículo de Visitante'),
        ('emergencia', 'Vehículo de Emergencia'),
    )
    
    # Información del vehículo
    placa_vehiculo = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^[A-Z0-9\-]{3,10}$', 'Formato de placa inválido')],
        verbose_name="Placa del Vehículo"
    )
    tipo_vehiculo = models.CharField(
        max_length=20,
        choices=TIPOS_VEHICULO,
        default='auto',
        verbose_name="Tipo de Vehículo"
    )
    marca = models.CharField(max_length=50, blank=True, verbose_name="Marca")
    modelo = models.CharField(max_length=50, blank=True, verbose_name="Modelo")
    color = models.CharField(max_length=30, blank=True, verbose_name="Color")
    año = models.PositiveIntegerField(null=True, blank=True, verbose_name="Año")
    
    # Propietario/Usuario
    propietario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vehiculos',
        verbose_name="Propietario"
    )
    unidad_asignada = models.ForeignKey(
        UnidadHabitacional,
        on_delete=models.CASCADE,
        related_name='vehiculos_autorizados',
        verbose_name="Unidad Asignada"
    )
    
    # Datos de IA y reconocimiento
    foto_vehiculo = models.ImageField(
        upload_to=upload_to_seguridad,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="Foto del Vehículo"
    )
    foto_placa = models.ImageField(
        upload_to=upload_to_seguridad,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="Foto de la Placa"
    )
    datos_ocr_json = models.JSONField(
        default=dict,
        blank=True,
        help_text="Datos de OCR de la placa en formato JSON",
        verbose_name="Datos OCR"
    )
    confianza_ocr = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Porcentaje de confianza del OCR",
        verbose_name="Confianza OCR (%)"
    )
    
    # Control de acceso
    estado_acceso = models.CharField(
        max_length=20,
        choices=ESTADOS_ACCESO,
        default='autorizado',
        verbose_name="Estado de Acceso"
    )
    es_vehiculo_residente = models.BooleanField(default=True, verbose_name="Es Vehículo de Residente")
    acceso_temporal_hasta = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Acceso Temporal Hasta"
    )
    
    # Información adicional
    numero_estacionamiento = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Número de Estacionamiento"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    # Registro
    registrado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vehiculos_registrados',
        verbose_name="Registrado por"
    )
    esta_activo = models.BooleanField(default=True, verbose_name="Está Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Acceso de Vehículo"
        verbose_name_plural = "Accesos de Vehículos"
        db_table = "accesos_vehiculos"
        ordering = ['-fecha_creacion']
        unique_together = ['placa_vehiculo', 'unidad_asignada']
        indexes = [
            models.Index(fields=['placa_vehiculo']),
            models.Index(fields=['estado_acceso']),
        ]
    
    def __str__(self):
        return f"{self.placa_vehiculo} - {self.propietario.get_full_name()}"

class RegistroAcceso(models.Model):
    """
    Registro de todos los accesos al condominio
    """
    TIPOS_ACCESO = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )
    
    METODOS_ACCESO = (
        ('facial', 'Reconocimiento Facial'),
        ('qr', 'Código QR'),
        ('manual', 'Manual'),
        ('tarjeta', 'Tarjeta de Acceso'),
        ('vehicular', 'Acceso Vehicular'),
        ('emergencia', 'Acceso de Emergencia'),
    )
    
    # Información del acceso
    tipo_acceso = models.CharField(
        max_length=10,
        choices=TIPOS_ACCESO,
        verbose_name="Tipo de Acceso"
    )
    metodo_acceso = models.CharField(
        max_length=20,
        choices=METODOS_ACCESO,
        verbose_name="Método de Acceso"
    )
    
    # Persona que accede
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registros_acceso',
        verbose_name="Usuario"
    )
    visitante = models.ForeignKey(
        RegistroVisitante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accesos',
        verbose_name="Visitante"
    )
    vehiculo = models.ForeignKey(
        AccesoVehiculo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accesos',
        verbose_name="Vehículo"
    )
    
    # Datos del acceso
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    ubicacion_acceso = models.CharField(
        max_length=100,
        default="Entrada Principal",
        verbose_name="Ubicación de Acceso"
    )
    
    # Datos de IA
    foto_acceso = models.ImageField(
        upload_to=upload_to_seguridad,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="Foto del Acceso"
    )
    datos_biometricos = models.JSONField(
        default=dict,
        blank=True,
        help_text="Datos biométricos capturados",
        verbose_name="Datos Biométricos"
    )
    confianza_identificacion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Confianza de Identificación (%)"
    )
    
    # Control y seguridad
    acceso_autorizado = models.BooleanField(default=True, verbose_name="Acceso Autorizado")
    requiere_atencion = models.BooleanField(default=False, verbose_name="Requiere Atención")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    # Sistema y logs
    dispositivo_origen = models.CharField(
        max_length=100,
        blank=True,
        help_text="Dispositivo que registró el acceso",
        verbose_name="Dispositivo de Origen"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")
    
    class Meta:
        verbose_name = "Registro de Acceso"
        verbose_name_plural = "Registros de Accesos"
        db_table = "registros_accesos"
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['fecha_hora']),
            models.Index(fields=['tipo_acceso']),
            models.Index(fields=['metodo_acceso']),
        ]
    
    def __str__(self):
        persona = self.usuario or self.visitante
        return f"{self.get_tipo_acceso_display()} - {persona} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"

class IncidenteSeguridad(models.Model):
    """
    Registro de incidentes de seguridad con detección de anomalías por IA
    """
    TIPOS_INCIDENTE = (
        ('intrusion', 'Intrusión Detectada'),
        ('acceso_no_autorizado', 'Acceso No Autorizado'),
        ('vehiculo_sospechoso', 'Vehículo Sospechoso'),
        ('persona_no_identificada', 'Persona No Identificada'),
        ('movimiento_anomalo', 'Movimiento Anómalo'),
        ('zona_restringida', 'Acceso a Zona Restringida'),
        ('emergencia', 'Situación de Emergencia'),
        ('vandalismo', 'Vandalismo'),
        ('otro', 'Otro Incidente'),
    )
    
    NIVELES_GRAVEDAD = (
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
        ('critico', 'Crítico'),
    )
    
    ESTADOS_INCIDENTE = (
        ('abierto', 'Abierto'),
        ('en_investigacion', 'En Investigación'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
        ('falsa_alarma', 'Falsa Alarma'),
    )
    
    # Información básica del incidente
    codigo_incidente = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name="Código del Incidente"
    )
    tipo_incidente = models.CharField(
        max_length=30,
        choices=TIPOS_INCIDENTE,
        verbose_name="Tipo de Incidente"
    )
    nivel_gravedad = models.CharField(
        max_length=10,
        choices=NIVELES_GRAVEDAD,
        default='medio',
        verbose_name="Nivel de Gravedad"
    )
    
    # Descripción y ubicación
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación")
    coordenadas_gps = models.CharField(
        max_length=50,
        blank=True,
        help_text="Coordenadas GPS (lat,lng)",
        verbose_name="Coordenadas GPS"
    )
    
    # Detección automática por IA
    detectado_por_ia = models.BooleanField(default=False, verbose_name="Detectado por IA")
    algoritmo_deteccion = models.CharField(
        max_length=100,
        blank=True,
        help_text="Algoritmo de IA que detectó el incidente",
        verbose_name="Algoritmo de Detección"
    )
    confianza_deteccion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Confianza de la detección automática (%)",
        verbose_name="Confianza de Detección (%)"
    )
    
    # Evidencia multimedia
    foto_incidente = models.ImageField(
        upload_to=upload_to_seguridad,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="Foto del Incidente"
    )
    video_incidente = models.FileField(
        upload_to=upload_to_seguridad,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov'])],
        verbose_name="Video del Incidente"
    )
    
    # Personas involucradas
    usuario_involucrado = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidentes_involucrado',
        verbose_name="Usuario Involucrado"
    )
    visitante_involucrado = models.ForeignKey(
        RegistroVisitante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidentes',
        verbose_name="Visitante Involucrado"
    )
    vehiculo_involucrado = models.ForeignKey(
        AccesoVehiculo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidentes',
        verbose_name="Vehículo Involucrado"
    )
    
    # Gestión del incidente
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_INCIDENTE,
        default='abierto',
        verbose_name="Estado"
    )
    reportado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='incidentes_reportados',
        verbose_name="Reportado por"
    )
    asignado_a = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidentes_asignados',
        verbose_name="Asignado a"
    )
    
    # Fechas y tiempos
    fecha_incidente = models.DateTimeField(verbose_name="Fecha del Incidente")
    fecha_reporte = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Reporte")
    fecha_resolucion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Resolución")
    
    # Seguimiento
    acciones_tomadas = models.TextField(blank=True, verbose_name="Acciones Tomadas")
    notas_seguimiento = models.TextField(blank=True, verbose_name="Notas de Seguimiento")
    
    # Metadatos de IA
    datos_analisis_ia = models.JSONField(
        default=dict,
        blank=True,
        help_text="Datos del análisis de IA en formato JSON",
        verbose_name="Datos de Análisis IA"
    )
    
    class Meta:
        verbose_name = "Incidente de Seguridad"
        verbose_name_plural = "Incidentes de Seguridad"
        db_table = "incidentes_seguridad"
        ordering = ['-fecha_incidente']
        indexes = [
            models.Index(fields=['tipo_incidente']),
            models.Index(fields=['nivel_gravedad']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_incidente']),
        ]
    
    def __str__(self):
        return f"{self.codigo_incidente} - {self.titulo}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_incidente:
            self.codigo_incidente = f"INC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class ConfiguracionIA(models.Model):
    """
    Configuración de los módulos de IA y visión artificial
    """
    TIPOS_ALGORITMO = (
        ('face_recognition', 'Reconocimiento Facial'),
        ('license_plate_ocr', 'OCR de Placas'),
        ('anomaly_detection', 'Detección de Anomalías'),
        ('object_detection', 'Detección de Objetos'),
        ('behavioral_analysis', 'Análisis de Comportamiento'),
        ('predictive_analytics', 'Analítica Predictiva'),
    )
    
    # Información del algoritmo
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    tipo_algoritmo = models.CharField(
        max_length=30,
        choices=TIPOS_ALGORITMO,
        verbose_name="Tipo de Algoritmo"
    )
    descripcion = models.TextField(verbose_name="Descripción")
    
    # Configuración técnica
    modelo_ia = models.CharField(
        max_length=200,
        help_text="Ruta o nombre del modelo de IA",
        verbose_name="Modelo de IA"
    )
    parametros_configuracion = models.JSONField(
        default=dict,
        help_text="Parámetros de configuración en formato JSON",
        verbose_name="Parámetros de Configuración"
    )
    umbral_confianza = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('80.00'),
        help_text="Umbral mínimo de confianza para considerar válida la detección",
        verbose_name="Umbral de Confianza (%)"
    )
    
    # Estado y rendimiento
    esta_activo = models.BooleanField(default=True, verbose_name="Está Activo")
    version_modelo = models.CharField(max_length=20, default="1.0", verbose_name="Versión del Modelo")
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    # Métricas de rendimiento
    precision_promedio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Precisión promedio del modelo (%)",
        verbose_name="Precisión Promedio (%)"
    )
    recall_promedio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Recall promedio del modelo (%)",
        verbose_name="Recall Promedio (%)"
    )
    tiempo_procesamiento_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Tiempo promedio de procesamiento en milisegundos",
        verbose_name="Tiempo de Procesamiento (ms)"
    )
    
    # Configuración de alertas
    generar_alertas = models.BooleanField(default=True, verbose_name="Generar Alertas")
    nivel_alerta_minimo = models.CharField(
        max_length=10,
        choices=IncidenteSeguridad.NIVELES_GRAVEDAD,
        default='medio',
        verbose_name="Nivel Mínimo de Alerta"
    )
    
    # Registro
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='configuraciones_ia_creadas',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Configuración de IA"
        verbose_name_plural = "Configuraciones de IA"
        db_table = "configuraciones_ia"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_algoritmo_display()}"

class AnalisisPredictivoMorosidad(models.Model):
    """
    Análisis predictivo de morosidad basado en IA
    """
    NIVELES_RIESGO = (
        ('muy_bajo', 'Muy Bajo'),
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
        ('muy_alto', 'Muy Alto'),
    )
    
    # Información de la predicción
    unidad = models.ForeignKey(
        UnidadHabitacional,
        on_delete=models.CASCADE,
        related_name='analisis_morosidad',
        verbose_name="Unidad"
    )
    usuario_analizado = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='analisis_morosidad',
        verbose_name="Usuario Analizado"
    )
    
    # Resultados del análisis
    probabilidad_morosidad = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Probabilidad de morosidad (%)",
        verbose_name="Probabilidad de Morosidad (%)"
    )
    nivel_riesgo = models.CharField(
        max_length=10,
        choices=NIVELES_RIESGO,
        verbose_name="Nivel de Riesgo"
    )
    
    # Factores del análisis
    factores_riesgo = models.JSONField(
        default=dict,
        help_text="Factores que contribuyen al riesgo en formato JSON",
        verbose_name="Factores de Riesgo"
    )
    historial_pagos_analizado = models.JSONField(
        default=dict,
        help_text="Resumen del historial de pagos analizado",
        verbose_name="Historial de Pagos Analizado"
    )
    
    # Recomendaciones
    recomendaciones = models.TextField(
        blank=True,
        help_text="Recomendaciones generadas por el sistema",
        verbose_name="Recomendaciones"
    )
    acciones_sugeridas = models.JSONField(
        default=list,
        help_text="Lista de acciones sugeridas",
        verbose_name="Acciones Sugeridas"
    )
    
    # Metadatos del análisis
    modelo_utilizado = models.CharField(
        max_length=100,
        help_text="Modelo de IA utilizado para el análisis",
        verbose_name="Modelo Utilizado"
    )
    version_modelo = models.CharField(max_length=20, verbose_name="Versión del Modelo")
    confianza_prediccion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Confianza en la predicción (%)",
        verbose_name="Confianza de la Predicción (%)"
    )
    
    # Seguimiento
    fecha_analisis = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Análisis")
    valido_hasta = models.DateTimeField(
        help_text="Fecha hasta la cual es válido el análisis",
        verbose_name="Válido Hasta"
    )
    fue_preciso = models.BooleanField(
        null=True,
        blank=True,
        help_text="Si la predicción fue precisa (se evalúa posteriormente)",
        verbose_name="Fue Preciso"
    )
    
    # Sistema
    generado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='analisis_generados',
        verbose_name="Generado por"
    )
    
    class Meta:
        verbose_name = "Análisis Predictivo de Morosidad"
        verbose_name_plural = "Análisis Predictivos de Morosidad"
        db_table = "analisis_predictivos_morosidad"
        ordering = ['-fecha_analisis']
        indexes = [
            models.Index(fields=['nivel_riesgo']),
            models.Index(fields=['fecha_analisis']),
        ]
    
    def __str__(self):
        return f"Análisis {self.unidad} - Riesgo: {self.get_nivel_riesgo_display()}"
