from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.autenticacion.models import Usuario

class UnidadHabitacional(models.Model):
    """
    Modelo para las unidades habitacionales del condominio
    """
    numero_unidad = models.CharField(max_length=10, unique=True, verbose_name="Número de Unidad")
    edificio = models.CharField(max_length=10, verbose_name="Edificio")
    propietario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='unidades_propias',
        verbose_name="Propietario"
    )
    inquilino = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='unidades_alquiladas',
        verbose_name="Inquilino"
    )
    area_m2 = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Área (m²)"
    )
    dormitorios = models.PositiveIntegerField(verbose_name="Número de Dormitorios")
    esta_activa = models.BooleanField(default=True, verbose_name="Está Activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Unidad Habitacional"
        verbose_name_plural = "Unidades Habitacionales"
        db_table = "unidades_habitacionales"
        ordering = ['edificio', 'numero_unidad']
    
    def __str__(self):
        return f"Unidad {self.numero_unidad} - Edificio {self.edificio}"
    
    @property
    def usuario_responsable(self):
        """Retorna el inquilino si existe, sino el propietario"""
        return self.inquilino if self.inquilino else self.propietario

class TipoPago(models.Model):
    """
    Catálogo de tipos de pagos
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    es_recurrente = models.BooleanField(default=True, verbose_name="Es Recurrente")
    monto_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Monto Base"
    )
    esta_activo = models.BooleanField(default=True, verbose_name="Está Activo")
    
    class Meta:
        verbose_name = "Tipo de Pago"
        verbose_name_plural = "Tipos de Pagos"
        db_table = "tipos_pagos"
    
    def __str__(self):
        return self.nombre

class Pago(models.Model):
    """
    Modelo principal para los pagos y cuotas
    """
    ESTADOS_PAGO = (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
        ('parcial', 'Pago Parcial'),
        ('cancelado', 'Cancelado'),
    )
    
    unidad = models.ForeignKey(
        UnidadHabitacional,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name="Unidad"
    )
    usuario_pagador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='pagos_realizados',
        verbose_name="Usuario que Paga"
    )
    tipo_pago = models.ForeignKey(
        TipoPago,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name="Tipo de Pago"
    )
    
    # Información del pago
    monto_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Monto Total"
    )
    monto_pagado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Monto Pagado"
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS_PAGO, 
        default='pendiente',
        verbose_name="Estado"
    )
    
    # Fechas importantes
    fecha_vencimiento = models.DateField(verbose_name="Fecha de Vencimiento")
    fecha_pago = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Pago")
    periodo = models.CharField(
        max_length=7,  # Formato: YYYY-MM
        help_text="Formato: YYYY-MM (ej: 2025-01)",
        verbose_name="Período"
    )
    
    # Información adicional
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    referencia_pago = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Referencia de Pago"
    )
    
    # Comprobante
    comprobante = models.ImageField(
        upload_to='comprobantes/', 
        null=True, 
        blank=True,
        verbose_name="Comprobante"
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pagos_creados',
        verbose_name="Creado por"
    )
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        db_table = "pagos"
        ordering = ['-fecha_vencimiento', '-fecha_creacion']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_vencimiento']),
            models.Index(fields=['periodo']),
            models.Index(fields=['unidad', 'periodo']),
        ]
    
    def __str__(self):
        return f"Pago {self.tipo_pago.nombre} - {self.unidad} - {self.periodo}"
    
    @property
    def saldo_pendiente(self):
        """Calcula el saldo pendiente"""
        return self.monto_total - self.monto_pagado
    
    @property
    def esta_vencido(self):
        """Verifica si el pago está vencido"""
        from django.utils import timezone
        return self.fecha_vencimiento < timezone.now().date() and self.estado == 'pendiente'
    
    @property
    def dias_vencido(self):
        """Calcula los días de vencimiento"""
        if self.esta_vencido:
            from django.utils import timezone
            return (timezone.now().date() - self.fecha_vencimiento).days
        return 0

class HistorialPago(models.Model):
    """
    Historial de transacciones y cambios de estado de pagos
    """
    pago = models.ForeignKey(
        Pago,
        on_delete=models.CASCADE,
        related_name='historial',
        verbose_name="Pago"
    )
    monto_transaccion = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Monto de la Transacción"
    )
    estado_anterior = models.CharField(max_length=20, verbose_name="Estado Anterior")
    estado_nuevo = models.CharField(max_length=20, verbose_name="Estado Nuevo")
    metodo_pago = models.CharField(
        max_length=50,
        choices=(
            ('efectivo', 'Efectivo'),
            ('transferencia', 'Transferencia Bancaria'),
            ('deposito', 'Depósito Bancario'),
            ('cheque', 'Cheque'),
            ('tarjeta', 'Tarjeta de Crédito/Débito'),
            ('qr', 'Código QR'),
            ('otro', 'Otro'),
        ),
        default='transferencia',
        verbose_name="Método de Pago"
    )
    referencia = models.CharField(max_length=100, blank=True, verbose_name="Referencia")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    procesado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Procesado por"
    )
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Historial de Pago"
        verbose_name_plural = "Historial de Pagos"
        db_table = "historial_pagos"
        ordering = ['-fecha_transaccion']
    
    def __str__(self):
        return f"Transacción {self.pago} - ${self.monto_transaccion}"

class Multa(models.Model):
    """
    Multas aplicadas a las unidades
    """
    TIPOS_MULTA = (
        ('retraso_pago', 'Retraso en Pago'),
        ('ruido', 'Ruido Excesivo'),
        ('mascotas', 'Incumplimiento Normas Mascotas'),
        ('areas_comunes', 'Mal Uso Áreas Comunes'),
        ('estacionamiento', 'Mal Uso Estacionamiento'),
        ('basura', 'Manejo Inadecuado de Basura'),
        ('otro', 'Otro'),
    )
    
    unidad = models.ForeignKey(
        UnidadHabitacional,
        on_delete=models.CASCADE,
        related_name='multas',
        verbose_name="Unidad"
    )
    tipo_multa = models.CharField(
        max_length=50,
        choices=TIPOS_MULTA,
        verbose_name="Tipo de Multa"
    )
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Monto"
    )
    descripcion = models.TextField(verbose_name="Descripción")
    fecha_infraccion = models.DateField(verbose_name="Fecha de Infracción")
    esta_pagada = models.BooleanField(default=False, verbose_name="Está Pagada")
    pago_asociado = models.ForeignKey(
        Pago,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Pago Asociado"
    )
    aplicada_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Aplicada por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Multa"
        verbose_name_plural = "Multas"
        db_table = "multas"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Multa {self.get_tipo_multa_display()} - {self.unidad}"