from django.db import models
from django.core.validators import FileExtensionValidator
from apps.autenticacion.models import Usuario
from apps.finanzas.models import UnidadHabitacional
import json

class CategoriaNotificacion(models.Model):
    """
    Categorías para organizar las notificaciones
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    color = models.CharField(
        max_length=7, 
        default='#007bff',
        help_text="Color hexadecimal (ej: #007bff)",
        verbose_name="Color"
    )
    icono = models.CharField(
        max_length=50, 
        default='bell',
        help_text="Icono de Font Awesome o similar",
        verbose_name="Icono"
    )
    prioridad = models.IntegerField(
        default=1,
        choices=[(1, 'Baja'), (2, 'Media'), (3, 'Alta'), (4, 'Crítica')],
        verbose_name="Prioridad"
    )
    esta_activa = models.BooleanField(default=True, verbose_name="Está Activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoría de Notificación"
        verbose_name_plural = "Categorías de Notificaciones"
        db_table = "categorias_notificaciones"
        ordering = ['-prioridad', 'nombre']
    
    def __str__(self):
        return self.nombre

class Notificacion(models.Model):
    """
    Sistema principal de notificaciones
    """
    TIPOS_DESTINATARIO = (
        ('todos', 'Todos los Usuarios'),
        ('residentes', 'Solo Residentes'),
        ('propietarios', 'Solo Propietarios'),
        ('inquilinos', 'Solo Inquilinos'),
        ('administradores', 'Solo Administradores'),
        ('seguridad', 'Personal de Seguridad'),
        ('mantenimiento', 'Personal de Mantenimiento'),
        ('edificio', 'Por Edificio'),
        ('unidades', 'Unidades Específicas'),
        ('usuarios', 'Usuarios Específicos'),
    )
    
    ESTADOS = (
        ('borrador', 'Borrador'),
        ('programada', 'Programada'),
        ('enviada', 'Enviada'),
        ('cancelada', 'Cancelada'),
    )
    
    # Información básica
    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensaje = models.TextField(verbose_name="Mensaje")
    categoria = models.ForeignKey(
        CategoriaNotificacion,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        verbose_name="Categoría"
    )
    
    # Configuración de envío
    tipo_destinatario = models.CharField(
        max_length=20,
        choices=TIPOS_DESTINATARIO,
        default='todos',
        verbose_name="Tipo de Destinatario"
    )
    usuarios_especificos = models.ManyToManyField(
        Usuario,
        through='DestinatarioNotificacion',
        related_name='notificaciones_recibidas',
        blank=True,
        verbose_name="Usuarios Específicos"
    )
    edificios_objetivo = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de edificios objetivo ['A', 'B', 'C']",
        verbose_name="Edificios Objetivo"
    )
    unidades_objetivo = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de IDs de unidades objetivo [1, 2, 3]",
        verbose_name="Unidades Objetivo"
    )
    
    # Configuración de notificación
    es_push = models.BooleanField(default=True, verbose_name="Notificación Push")
    es_email = models.BooleanField(default=False, verbose_name="Enviar Email")
    es_sms = models.BooleanField(default=False, verbose_name="Enviar SMS")
    es_urgente = models.BooleanField(default=False, verbose_name="Es Urgente")
    
    # Programación
    enviar_inmediatamente = models.BooleanField(default=True, verbose_name="Enviar Inmediatamente")
    fecha_programada = models.DateTimeField(null=True, blank=True, verbose_name="Fecha Programada")
    fecha_expiracion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Expiración")
    
    # Archivos adjuntos
    imagen = models.ImageField(
        upload_to='notificaciones/imagenes/', 
        null=True, 
        blank=True,
        verbose_name="Imagen"
    )
    archivo_adjunto = models.FileField(
        upload_to='notificaciones/archivos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png'])],
        verbose_name="Archivo Adjunto"
    )
    
    # Configuración adicional
    requiere_confirmacion = models.BooleanField(default=False, verbose_name="Requiere Confirmación")
    metadatos = models.JSONField(
        default=dict,
        blank=True,
        help_text="Datos adicionales en formato JSON",
        verbose_name="Metadatos"
    )
    
    # Estado y seguimiento
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='borrador',
        verbose_name="Estado"
    )
    total_destinatarios = models.PositiveIntegerField(default=0, verbose_name="Total Destinatarios")
    total_enviados = models.PositiveIntegerField(default=0, verbose_name="Total Enviados")
    total_leidos = models.PositiveIntegerField(default=0, verbose_name="Total Leídos")
    total_confirmados = models.PositiveIntegerField(default=0, verbose_name="Total Confirmados")
    
    # Información del creador
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificaciones_creadas',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_envio = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Envío")
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        db_table = "notificaciones"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['tipo_destinatario']),
            models.Index(fields=['fecha_programada']),
            models.Index(fields=['es_urgente']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.get_estado_display()}"
    
    @property
    def tasa_apertura(self):
        """Calcula la tasa de apertura de la notificación"""
        if self.total_enviados == 0:
            return 0
        return round((self.total_leidos / self.total_enviados) * 100, 2)
    
    @property
    def tasa_confirmacion(self):
        """Calcula la tasa de confirmación si aplica"""
        if not self.requiere_confirmacion or self.total_enviados == 0:
            return 0
        return round((self.total_confirmados / self.total_enviados) * 100, 2)

class DestinatarioNotificacion(models.Model):
    """
    Tabla intermedia para tracking individual de notificaciones
    """
    ESTADOS_LECTURA = (
        ('no_enviado', 'No Enviado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('leido', 'Leído'),
        ('confirmado', 'Confirmado'),
        ('error', 'Error al Enviar'),
    )
    
    notificacion = models.ForeignKey(
        Notificacion,
        on_delete=models.CASCADE,
        related_name='destinatarios',
        verbose_name="Notificación"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificaciones_destinatario',
        verbose_name="Usuario"
    )
    
    # Estado del envío
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_LECTURA,
        default='no_enviado',
        verbose_name="Estado"
    )
    
    # Fechas de seguimiento
    fecha_envio = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Envío")
    fecha_entrega = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Entrega")
    fecha_lectura = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Lectura")
    fecha_confirmacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    
    # Información adicional
    dispositivo_lectura = models.CharField(
        max_length=20,
        choices=[('web', 'Web'), ('movil', 'Móvil'), ('email', 'Email')],
        null=True,
        blank=True,
        verbose_name="Dispositivo de Lectura"
    )
    mensaje_error = models.TextField(blank=True, verbose_name="Mensaje de Error")
    token_confirmacion = models.CharField(max_length=100, blank=True, verbose_name="Token de Confirmación")
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Destinatario de Notificación"
        verbose_name_plural = "Destinatarios de Notificaciones"
        db_table = "destinatarios_notificaciones"
        unique_together = ['notificacion', 'usuario']
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_lectura']),
        ]
    
    def __str__(self):
        return f"{self.notificacion.titulo} -> {self.usuario.email}"

class AvisoGeneral(models.Model):
    """
    Avisos generales del condominio (tablón de anuncios)
    """
    TIPOS_AVISO = (
        ('informativo', 'Informativo'),
        ('importante', 'Importante'), 
        ('urgente', 'Urgente'),
        ('mantenimiento', 'Mantenimiento'),
        ('reunion', 'Reunión'),
        ('evento', 'Evento'),
        ('cambio_reglamento', 'Cambio de Reglamento'),
    )
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    contenido = models.TextField(verbose_name="Contenido")
    tipo_aviso = models.CharField(
        max_length=20,
        choices=TIPOS_AVISO,
        default='informativo',
        verbose_name="Tipo de Aviso"
    )
    
    # Configuración de visibilidad
    es_destacado = models.BooleanField(default=False, verbose_name="Es Destacado")
    mostrar_en_inicio = models.BooleanField(default=True, verbose_name="Mostrar en Inicio")
    requiere_notificacion = models.BooleanField(default=True, verbose_name="Crear Notificación")
    
    # Fechas
    fecha_inicio = models.DateTimeField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Fin")
    
    # Archivos
    imagen_portada = models.ImageField(
        upload_to='avisos/portadas/', 
        null=True, 
        blank=True,
        verbose_name="Imagen de Portada"
    )
    archivo_adjunto = models.FileField(
        upload_to='avisos/archivos/',
        null=True,
        blank=True,
        verbose_name="Archivo Adjunto"
    )
    
    # Configuración de destinatarios (similar a notificaciones)
    dirigido_a = models.CharField(
        max_length=20,
        choices=Notificacion.TIPOS_DESTINATARIO,
        default='todos',
        verbose_name="Dirigido a"
    )
    edificios_objetivo = models.JSONField(default=list, blank=True)
    
    # Seguimiento
    visualizaciones = models.PositiveIntegerField(default=0, verbose_name="Visualizaciones")
    likes = models.PositiveIntegerField(default=0, verbose_name="Me Gusta")
    
    # Estado
    esta_activo = models.BooleanField(default=True, verbose_name="Está Activo")
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='avisos_creados',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Aviso General"
        verbose_name_plural = "Avisos Generales"
        db_table = "avisos_generales"
        ordering = ['-es_destacado', '-fecha_creacion']
        indexes = [
            models.Index(fields=['tipo_aviso']),
            models.Index(fields=['esta_activo']),
            models.Index(fields=['fecha_inicio']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_aviso_display()}"
    
    @property
    def esta_vigente(self):
        """Verifica si el aviso está vigente"""
        from django.utils import timezone
        now = timezone.now()
        
        if self.fecha_fin:
            return self.fecha_inicio <= now <= self.fecha_fin
        return self.fecha_inicio <= now

class InteraccionAviso(models.Model):
    """
    Interacciones de los usuarios con los avisos (likes, visualizaciones)
    """
    TIPOS_INTERACCION = (
        ('visualizacion', 'Visualización'),
        ('like', 'Me Gusta'),
        ('dislike', 'No Me Gusta'),
        ('compartir', 'Compartir'),
    )
    
    aviso = models.ForeignKey(
        AvisoGeneral,
        on_delete=models.CASCADE,
        related_name='interacciones',
        verbose_name="Aviso"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='interacciones_avisos',
        verbose_name="Usuario"
    )
    tipo_interaccion = models.CharField(
        max_length=20,
        choices=TIPOS_INTERACCION,
        verbose_name="Tipo de Interacción"
    )
    fecha_interaccion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Interacción con Aviso"
        verbose_name_plural = "Interacciones con Avisos"
        db_table = "interacciones_avisos"
        unique_together = ['aviso', 'usuario', 'tipo_interaccion']
    
    def __str__(self):
        return f"{self.usuario.email} - {self.get_tipo_interaccion_display()} - {self.aviso.titulo}"

class ConfiguracionNotificacion(models.Model):
    """
    Configuración personalizada de notificaciones por usuario
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='config_notificaciones',
        verbose_name="Usuario"
    )
    
    # Configuraciones generales
    recibir_push = models.BooleanField(default=True, verbose_name="Recibir Notificaciones Push")
    recibir_email = models.BooleanField(default=True, verbose_name="Recibir Emails")
    recibir_sms = models.BooleanField(default=False, verbose_name="Recibir SMS")
    
    # Configuraciones por categoría
    notif_pagos = models.BooleanField(default=True, verbose_name="Notificaciones de Pagos")
    notif_mantenimiento = models.BooleanField(default=True, verbose_name="Notificaciones de Mantenimiento")
    notif_seguridad = models.BooleanField(default=True, verbose_name="Notificaciones de Seguridad")
    notif_eventos = models.BooleanField(default=True, verbose_name="Notificaciones de Eventos")
    notif_avisos = models.BooleanField(default=True, verbose_name="Avisos Generales")
    notif_reservas = models.BooleanField(default=True, verbose_name="Notificaciones de Reservas")
    
    # Configuraciones de horario
    horario_inicio = models.TimeField(default='07:00', verbose_name="Hora de Inicio")
    horario_fin = models.TimeField(default='22:00', verbose_name="Hora de Fin")
    no_molestar_fines_semana = models.BooleanField(default=False, verbose_name="No Molestar Fines de Semana")
    
    # Tokens para notificaciones push
    token_fcm_android = models.TextField(blank=True, verbose_name="Token FCM Android")
    token_fcm_ios = models.TextField(blank=True, verbose_name="Token FCM iOS")
    token_fcm_web = models.TextField(blank=True, verbose_name="Token FCM Web")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de Notificaciones"
        verbose_name_plural = "Configuraciones de Notificaciones"
        db_table = "configuraciones_notificaciones"
    
    def __str__(self):
        return f"Config. {self.usuario.email}"

class PlantillaNotificacion(models.Model):
    """
    Plantillas predefinidas para notificaciones comunes
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    
    # Contenido de la plantilla
    titulo_plantilla = models.CharField(max_length=200, verbose_name="Título (Plantilla)")
    mensaje_plantilla = models.TextField(verbose_name="Mensaje (Plantilla)")
    
    # Variables disponibles (JSON con descripción de variables)
    variables_disponibles = models.JSONField(
        default=dict,
        help_text="Variables que se pueden usar: {usuario}, {unidad}, {fecha}, etc.",
        verbose_name="Variables Disponibles"
    )
    
    # Configuración por defecto
    categoria_default = models.ForeignKey(
        CategoriaNotificacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoría por Defecto"
    )
    es_push_default = models.BooleanField(default=True, verbose_name="Push por Defecto")
    es_email_default = models.BooleanField(default=False, verbose_name="Email por Defecto")
    
    # Metadatos
    es_sistema = models.BooleanField(default=False, verbose_name="Es del Sistema")
    esta_activa = models.BooleanField(default=True, verbose_name="Está Activa")
    uso_contador = models.PositiveIntegerField(default=0, verbose_name="Veces Utilizada")
    
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='plantillas_creadas',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Plantilla de Notificación"
        verbose_name_plural = "Plantillas de Notificaciones"
        db_table = "plantillas_notificaciones"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def renderizar(self, **kwargs):
        """
        Renderiza la plantilla con las variables proporcionadas
        """
        titulo = self.titulo_plantilla
        mensaje = self.mensaje_plantilla
        
        for key, value in kwargs.items():
            titulo = titulo.replace(f'{{{key}}}', str(value))
            mensaje = mensaje.replace(f'{{{key}}}', str(value))
        
        return {
            'titulo': titulo,
            'mensaje': mensaje
        }