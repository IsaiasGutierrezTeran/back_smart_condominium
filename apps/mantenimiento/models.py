from django.db import models
from django.conf import settings

class TipoSolicitud(models.Model):
    """Tipos de solicitudes de mantenimiento"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    esta_activo = models.BooleanField(default=True)
    prioridad_default = models.CharField(
        max_length=20,
        choices=[
            ('baja', 'Baja'),
            ('media', 'Media'),
            ('alta', 'Alta'),
            ('critica', 'Crítica')
        ],
        default='media'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tipo de Solicitud"
        verbose_name_plural = "Tipos de Solicitud"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class SolicitudMantenimiento(models.Model):
    """Solicitudes de mantenimiento"""
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ]
    
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica')
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_solicitud = models.ForeignKey(TipoSolicitud, on_delete=models.CASCADE, related_name='solicitudes')
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes_mantenimiento')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='media')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='solicitudes_asignadas'
    )
    notas_internas = models.TextField(blank=True)
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_real = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name = "Solicitud de Mantenimiento"
        verbose_name_plural = "Solicitudes de Mantenimiento"
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"{self.titulo} - {self.estado}"

class ReporteMantenimiento(models.Model):
    """Reportes de mantenimiento realizados"""
    TIPOS_REPORTE = [
        ('preventivo', 'Mantenimiento Preventivo'),
        ('correctivo', 'Mantenimiento Correctivo'),
        ('inspeccion', 'Inspección'),
        ('otro', 'Otro')
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_reporte = models.CharField(max_length=20, choices=TIPOS_REPORTE, default='correctivo')
    solicitud_relacionada = models.ForeignKey(
        SolicitudMantenimiento, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reportes'
    )
    encargado = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='reportes_mantenimiento'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_mantenimiento = models.DateTimeField()
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    materiales_utilizados = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Reporte de Mantenimiento"
        verbose_name_plural = "Reportes de Mantenimiento"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_mantenimiento.strftime('%d/%m/%Y')}"
