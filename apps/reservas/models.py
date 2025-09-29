from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime, timedelta
from apps.autenticacion.models import Usuario
from apps.finanzas.models import UnidadHabitacional
import json


class TipoAreaComun(models.Model):
    """
    Categorización de las áreas comunes
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    icono = models.CharField(
        max_length=50, 
        default='home',
        help_text="Icono de Font Awesome o similar",
        verbose_name="Icono"
    )
    color = models.CharField(
        max_length=7, 
        default='#007bff',
        help_text="Color hexadecimal (ej: #007bff)",
        verbose_name="Color"
    )
    requiere_deposito = models.BooleanField(default=False, verbose_name="Requiere Depósito")
    permite_equipos_externos = models.BooleanField(default=True, verbose_name="Permite Equipos Externos")
    esta_activo = models.BooleanField(default=True, verbose_name="Está Activo")
    orden = models.PositiveIntegerField(default=1, verbose_name="Orden de Visualización")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tipo de Área Común"
        verbose_name_plural = "Tipos de Áreas Comunes"
        db_table = "tipos_areas_comunes"
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre

class AreaComun(models.Model):
    """
    Áreas comunes disponibles para reserva
    """
    ESTADOS = (
        ('disponible', 'Disponible'),
        ('mantenimiento', 'En Mantenimiento'),
        ('inhabilitada', 'Inhabilitada'),
        ('reservada_admin', 'Reservada por Administración'),
    )
    
    # Información básica
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    tipo_area = models.ForeignKey(
        TipoAreaComun,
        on_delete=models.CASCADE,
        related_name='areas',
        verbose_name="Tipo de Área"
    )
    
    # Capacidad y características
    capacidad_maxima = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Capacidad Máxima"
    )
    area_m2 = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Área (m²)"
    )
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación")
    
    # Configuración de reservas
    permite_reservas = models.BooleanField(default=True, verbose_name="Permite Reservas")
    tiempo_minimo_reserva = models.PositiveIntegerField(
        default=60,  # minutos
        help_text="Tiempo mínimo de reserva en minutos",
        verbose_name="Tiempo Mínimo (min)"
    )
    tiempo_maximo_reserva = models.PositiveIntegerField(
        default=480,  # 8 horas
        help_text="Tiempo máximo de reserva en minutos",
        verbose_name="Tiempo Máximo (min)"
    )
    anticipacion_minima = models.PositiveIntegerField(
        default=60,  # 1 hora
        help_text="Anticipación mínima en minutos",
        verbose_name="Anticipación Mínima (min)"
    )
    anticipacion_maxima = models.PositiveIntegerField(
        default=43200,  # 30 días
        help_text="Anticipación máxima en minutos",
        verbose_name="Anticipación Máxima (min)"
    )
    
    # Horarios de funcionamiento
    horario_funcionamiento = models.JSONField(
        default=dict,
        help_text="""
        Formato: {
            "lunes": {"inicio": "08:00", "fin": "22:00", "activo": true},
            "martes": {"inicio": "08:00", "fin": "22:00", "activo": true},
            ...
        }
        """,
        verbose_name="Horario de Funcionamiento"
    )
    
    # Tarifas
    tarifa_por_hora = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Tarifa por Hora"
    )
    tarifa_fin_semana = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Tarifa Fin de Semana"
    )
    deposito_garantia = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Depósito de Garantía"
    )
    
    # Configuración adicional
    requiere_autorizacion = models.BooleanField(default=False, verbose_name="Requiere Autorización")
    permite_decoracion = models.BooleanField(default=True, verbose_name="Permite Decoración")
    permite_musica = models.BooleanField(default=True, verbose_name="Permite Música")
    permite_comida_externa = models.BooleanField(default=True, verbose_name="Permite Comida Externa")
    incluye_mobiliario = models.BooleanField(default=False, verbose_name="Incluye Mobiliario")
    incluye_audio = models.BooleanField(default=False, verbose_name="Incluye Audio")
    incluye_iluminacion = models.BooleanField(default=False, verbose_name="Incluye Iluminación")
    
    # Reglas y restricciones
    reglas_uso = models.TextField(
        blank=True,
        help_text="Reglas específicas para el uso del área",
        verbose_name="Reglas de Uso"
    )
    equipamiento_incluido = models.JSONField(
        default=list,
        help_text="Lista de equipamiento incluido",
        verbose_name="Equipamiento Incluido"
    )
    restricciones_especiales = models.TextField(
        blank=True,
        verbose_name="Restricciones Especiales"
    )
    
    # Estado y disponibilidad
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='disponible',
        verbose_name="Estado"
    )
    fecha_inicio_inhabilitacion = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Inicio Inhabilitación"
    )
    fecha_fin_inhabilitacion = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fin Inhabilitación"
    )
    motivo_inhabilitacion = models.TextField(
        blank=True,
        verbose_name="Motivo de Inhabilitación"
    )
    
    # Imágenes
    imagen_principal = models.ImageField(
        upload_to='areas_comunes/',
        null=True,
        blank=True,
        verbose_name="Imagen Principal"
    )
    
    # Estadísticas
    total_reservas = models.PositiveIntegerField(default=0, verbose_name="Total Reservas")
    rating_promedio = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))],
        verbose_name="Rating Promedio"
    )
    
    # Metadatos
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='areas_creadas',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Área Común"
        verbose_name_plural = "Áreas Comunes"
        db_table = "areas_comunes"
        ordering = ['tipo_area__orden', 'nombre']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['tipo_area']),
            models.Index(fields=['permite_reservas']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo_area.nombre})"
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.tiempo_minimo_reserva >= self.tiempo_maximo_reserva:
            raise ValidationError("El tiempo mínimo debe ser menor al tiempo máximo")
        
        if self.anticipacion_minima >= self.anticipacion_maxima:
            raise ValidationError("La anticipación mínima debe ser menor a la máxima")
        
        if self.tarifa_fin_semana and self.tarifa_fin_semana < self.tarifa_por_hora:
            raise ValidationError("La tarifa de fin de semana no puede ser menor a la tarifa regular")
    
    @property
    def esta_disponible(self):
        """Verifica si el área está disponible para reservas"""
        if not self.permite_reservas:
            return False
        
        if self.estado != 'disponible':
            return False
        
        # Verificar si está en período de inhabilitación
        if self.fecha_inicio_inhabilitacion and self.fecha_fin_inhabilitacion:
            from django.utils import timezone
            now = timezone.now()
            if self.fecha_inicio_inhabilitacion <= now <= self.fecha_fin_inhabilitacion:
                return False
        
        return True
    
    @property
    def tarifa_actual(self):
        """Obtiene la tarifa actual según el día"""
        from datetime import datetime
        if datetime.now().weekday() >= 5 and self.tarifa_fin_semana:  # Sábado y Domingo
            return self.tarifa_fin_semana
        return self.tarifa_por_hora
    
    def esta_disponible_en_horario(self, fecha_hora):
        """Verifica si está disponible en un horario específico"""
        if not self.esta_disponible:
            return False
        
        dia_semana = [
            'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'
        ][fecha_hora.weekday()]
        
        horario_dia = self.horario_funcionamiento.get(dia_semana, {})
        if not horario_dia.get('activo', False):
            return False
        
        hora_inicio = datetime.strptime(horario_dia.get('inicio', '00:00'), '%H:%M').time()
        hora_fin = datetime.strptime(horario_dia.get('fin', '23:59'), '%H:%M').time()
        
        return hora_inicio <= fecha_hora.time() <= hora_fin

class Reserva(models.Model):
    """
    Reservas de áreas comunes
    """
    ESTADOS = (
        ('pendiente', 'Pendiente de Aprobación'),
        ('confirmada', 'Confirmada'),
        ('en_uso', 'En Uso'),
        ('completada', 'Completada'),
        ('cancelada_usuario', 'Cancelada por Usuario'),
        ('cancelada_admin', 'Cancelada por Administrador'),
        ('no_show', 'No se Presentó'),
    )
    
    TIPOS_EVENTO = (
        ('familiar', 'Evento Familiar'),
        ('social', 'Evento Social'),
        ('corporativo', 'Evento Corporativo'),
        ('deportivo', 'Evento Deportivo'),
        ('educativo', 'Evento Educativo'),
        ('religioso', 'Evento Religioso'),
        ('otro', 'Otro'),
    )
    
    # Información básica
    area_comun = models.ForeignKey(
        AreaComun,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name="Área Común"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name="Usuario"
    )
    unidad = models.ForeignKey(
        UnidadHabitacional,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name="Unidad"
    )
    
    # Fechas y horarios
    fecha_reserva = models.DateField(verbose_name="Fecha de la Reserva")
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    duracion_minutos = models.PositiveIntegerField(verbose_name="Duración (minutos)")
    
    # Información del evento
    tipo_evento = models.CharField(
        max_length=20,
        choices=TIPOS_EVENTO,
        default='familiar',
        verbose_name="Tipo de Evento"
    )
    nombre_evento = models.CharField(max_length=200, verbose_name="Nombre del Evento")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    numero_invitados = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Número de Invitados"
    )
    
    # Servicios adicionales
    requiere_decoracion = models.BooleanField(default=False, verbose_name="Requiere Decoración")
    requiere_audio = models.BooleanField(default=False, verbose_name="Requiere Audio")
    requiere_iluminacion = models.BooleanField(default=False, verbose_name="Requiere Iluminación")
    requiere_seguridad = models.BooleanField(default=False, verbose_name="Requiere Seguridad")
    requiere_limpieza_extra = models.BooleanField(default=False, verbose_name="Requiere Limpieza Extra")
    
    # Información de contacto
    telefono_contacto = models.CharField(max_length=20, verbose_name="Teléfono de Contacto")
    email_contacto = models.EmailField(blank=True, verbose_name="Email de Contacto")
    contacto_emergencia = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="Contacto de Emergencia"
    )
    
    # Costos
    costo_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Costo Base"
    )
    costo_servicios_adicionales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Costo Servicios Adicionales"
    )
    deposito_garantia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Depósito de Garantía"
    )
    costo_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Costo Total"
    )
    
    # Estado y seguimiento
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
        verbose_name="Estado"
    )
    requiere_aprobacion = models.BooleanField(default=False, verbose_name="Requiere Aprobación")
    aprobado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservas_aprobadas',
        verbose_name="Aprobado por"
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Aprobación")
    
    # Observaciones y notas
    observaciones_usuario = models.TextField(
        blank=True,
        verbose_name="Observaciones del Usuario"
    )
    observaciones_admin = models.TextField(
        blank=True,
        verbose_name="Observaciones de Administración"
    )
    motivo_cancelacion = models.TextField(
        blank=True,
        verbose_name="Motivo de Cancelación"
    )
    
    # Calificación del servicio
    calificacion = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Calificación (1-5)"
    )
    comentario_calificacion = models.TextField(
        blank=True,
        verbose_name="Comentario de Calificación"
    )
    fecha_calificacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Calificación"
    )
    
    # Metadatos
    codigo_reserva = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name="Código de Reserva"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        db_table = "reservas"
        ordering = ['-fecha_reserva', '-hora_inicio']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_reserva']),
            models.Index(fields=['area_comun', 'fecha_reserva']),
            models.Index(fields=['usuario']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(hora_inicio__lt=models.F('hora_fin')),
                name='hora_inicio_menor_hora_fin'
            ),
        ]
    
    def save(self, *args, **kwargs):
        # Generar código de reserva automáticamente
        if not self.codigo_reserva:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.codigo_reserva = f"RES-{timestamp[-8:]}"
        
        # Calcular duración en minutos
        if self.hora_inicio and self.hora_fin:
            inicio = datetime.combine(self.fecha_reserva, self.hora_inicio)
            fin = datetime.combine(self.fecha_reserva, self.hora_fin)
            self.duracion_minutos = int((fin - inicio).total_seconds() / 60)
        
        # Calcular costo total automáticamente
        self.calcular_costo_total()
        
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.fecha_reserva and self.hora_inicio and self.hora_fin:
            # Validar que la hora de inicio sea menor que la de fin
            if self.hora_inicio >= self.hora_fin:
                raise ValidationError("La hora de inicio debe ser menor a la hora de fin")
            
            # Validar duración mínima y máxima
            inicio = datetime.combine(self.fecha_reserva, self.hora_inicio)
            fin = datetime.combine(self.fecha_reserva, self.hora_fin)
            duracion_minutos = (fin - inicio).total_seconds() / 60
            
            if duracion_minutos < self.area_comun.tiempo_minimo_reserva:
                raise ValidationError(
                    f"La duración mínima es de {self.area_comun.tiempo_minimo_reserva} minutos"
                )
            
            if duracion_minutos > self.area_comun.tiempo_maximo_reserva:
                raise ValidationError(
                    f"La duración máxima es de {self.area_comun.tiempo_maximo_reserva} minutos"
                )
            
            # Validar anticipación
            from django.utils import timezone
            now = timezone.now()
            fecha_reserva_dt = datetime.combine(self.fecha_reserva, self.hora_inicio)
            
            if timezone.is_naive(fecha_reserva_dt):
                fecha_reserva_dt = timezone.make_aware(fecha_reserva_dt)
            
            anticipacion_minutos = (fecha_reserva_dt - now).total_seconds() / 60
            
            if anticipacion_minutos < self.area_comun.anticipacion_minima:
                raise ValidationError(
                    f"Debe reservar con al menos {self.area_comun.anticipacion_minima} minutos de anticipación"
                )
            
            if anticipacion_minutos > self.area_comun.anticipacion_maxima:
                raise ValidationError(
                    f"No puede reservar con más de {self.area_comun.anticipacion_maxima} minutos de anticipación"
                )
            
            # Validar capacidad
            if self.numero_invitados > self.area_comun.capacidad_maxima:
                raise ValidationError(
                    f"El número de invitados no puede exceder la capacidad máxima ({self.area_comun.capacidad_maxima})"
                )
            
            # Validar disponibilidad del área
            if not self.area_comun.esta_disponible_en_horario(fecha_reserva_dt):
                raise ValidationError("El área no está disponible en el horario seleccionado")
        
        # Validar que el usuario tenga una unidad asociada
        if not hasattr(self.usuario, 'perfil') or not self.usuario.perfil.numero_unidad:
            # Buscar unidad del usuario
            unidades_usuario = UnidadHabitacional.objects.filter(
                models.Q(propietario=self.usuario) | models.Q(inquilino=self.usuario)
            )
            if not unidades_usuario.exists():
                raise ValidationError("El usuario debe tener una unidad asociada para hacer reservas")
    
    def calcular_costo_total(self):
        """Calcula el costo total de la reserva"""
        if not self.area_comun or not self.duracion_minutos:
            return
        
        # Costo base por horas
        horas = self.duracion_minutos / 60
        
        # Determinar tarifa (normal o fin de semana)
        if self.fecha_reserva.weekday() >= 5 and self.area_comun.tarifa_fin_semana:  # Sábado y Domingo
            tarifa = self.area_comun.tarifa_fin_semana
        else:
            tarifa = self.area_comun.tarifa_por_hora
        
        self.costo_base = tarifa * Decimal(str(horas))
        
        # Servicios adicionales (esto se puede personalizar según necesidades)
        servicios = Decimal('0.00')
        if self.requiere_decoracion:
            servicios += Decimal('50.00')  # Ejemplo
        if self.requiere_audio:
            servicios += Decimal('30.00')  # Ejemplo
        if self.requiere_iluminacion:
            servicios += Decimal('20.00')  # Ejemplo
        if self.requiere_seguridad:
            servicios += Decimal('100.00')  # Ejemplo
        if self.requiere_limpieza_extra:
            servicios += Decimal('40.00')  # Ejemplo
        
        self.costo_servicios_adicionales = servicios
        
        # Depósito de garantía
        self.deposito_garantia = self.area_comun.deposito_garantia
        
        # Costo total
        self.costo_total = self.costo_base + self.costo_servicios_adicionales + self.deposito_garantia
    
    def puede_ser_cancelada(self):
        """Verifica si la reserva puede ser cancelada"""
        if self.estado in ['cancelada_usuario', 'cancelada_admin', 'completada']:
            return False
        
        from django.utils import timezone
        fecha_reserva_dt = datetime.combine(self.fecha_reserva, self.hora_inicio)
        if timezone.is_naive(fecha_reserva_dt):
            fecha_reserva_dt = timezone.make_aware(fecha_reserva_dt)
        
        # Permitir cancelar hasta 2 horas antes
        return fecha_reserva_dt > timezone.now() + timedelta(hours=2)
    
    def __str__(self):
        return f"{self.codigo_reserva} - {self.area_comun.nombre} - {self.fecha_reserva}"

class ImagenAreaComun(models.Model):
    """
    Imágenes adicionales de las áreas comunes
    """
    area_comun = models.ForeignKey(
        AreaComun,
        on_delete=models.CASCADE,
        related_name='imagenes',
        verbose_name="Área Común"
    )
    imagen = models.ImageField(
        upload_to='areas_comunes/galeria/',
        verbose_name="Imagen"
    )
    titulo = models.CharField(max_length=200, blank=True, verbose_name="Título")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    es_portada = models.BooleanField(default=False, verbose_name="Es Portada")
    orden = models.PositiveIntegerField(default=1, verbose_name="Orden")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Imagen de Área Común"
        verbose_name_plural = "Imágenes de Áreas Comunes"
        db_table = "imagenes_areas_comunes"
        ordering = ['orden', 'fecha_creacion']
    
    def __str__(self):
        return f"{self.area_comun.nombre} - Imagen {self.orden}"

class ServicioAdicional(models.Model):
    """
    Servicios adicionales que se pueden contratar con las reservas
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Precio"
    )
    unidad = models.CharField(
        max_length=50,
        default='por servicio',
        help_text="Ej: por hora, por servicio, por persona",
        verbose_name="Unidad"
    )
    areas_aplicables = models.ManyToManyField(
        AreaComun,
        related_name='servicios_disponibles',
        blank=True,
        verbose_name="Áreas Aplicables"
    )
    requiere_anticipacion = models.PositiveIntegerField(
        default=24,
        help_text="Horas de anticipación requeridas",
        verbose_name="Anticipación Requerida (horas)"
    )
    esta_activo = models.BooleanField(default=True, verbose_name="Está Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Servicio Adicional"
        verbose_name_plural = "Servicios Adicionales"
        db_table = "servicios_adicionales"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class ReservaServicio(models.Model):
    """
    Servicios adicionales contratados en una reserva
    """
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name='servicios_contratados',
        verbose_name="Reserva"
    )
    servicio = models.ForeignKey(
        ServicioAdicional,
        on_delete=models.CASCADE,
        verbose_name="Servicio"
    )
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Precio Unitario"
    )
    precio_total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Precio Total"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    fecha_contratacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Servicio de Reserva"
    verbose_name_plural = "Servicios de Reservas"
    db_table = "reservas_servicios"
    unique_together = ['reserva', 'servicio']

def save(self, *args, **kwargs):
    self.precio_total = self.precio_unitario * self.cantidad
    super().save(*args, **kwargs)

def __str__(self):
    return f"{self.reserva.codigo_reserva} - {self.servicio.nombre}"
class DisponibilidadEspecial(models.Model):
    """
    Fechas especiales que afectan la disponibilidad de las áreas comunes
    """
    TIPOS = (
        ('feriado', 'Feriado'),
        ('evento_especial', 'Evento Especial'),
        ('mantenimiento_programado', 'Mantenimiento Programado'),
        ('reserva_admin', 'Reserva Administrativa'),
    )
    
    area_comun = models.ForeignKey(
        AreaComun,
        on_delete=models.CASCADE,
        related_name='disponibilidades_especiales',
        verbose_name="Área Común"
    )
    tipo = models.CharField(max_length=30, choices=TIPOS, verbose_name="Tipo")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    fecha_inicio = models.DateTimeField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateTimeField(verbose_name="Fecha de Fin")
    esta_disponible = models.BooleanField(
        default=False,
        help_text="Si está marcado, el área estará disponible en estas fechas. Si no, estará bloqueada.",
        verbose_name="Está Disponible"
    )
    tarifa_especial = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Tarifa Especial"
    )
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Disponibilidad Especial"
        verbose_name_plural = "Disponibilidades Especiales"
        db_table = "disponibilidades_especiales"
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"{self.area_comun.nombre} - {self.titulo}"