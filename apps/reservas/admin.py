from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from .models import (
    TipoAreaComun, AreaComun, Reserva, ImagenAreaComun,
    ServicioAdicional, ReservaServicio, DisponibilidadEspecial
)

@admin.register(TipoAreaComun)
class AdminTipoAreaComun(admin.ModelAdmin):
    list_display = ['nombre', 'color_preview', 'icono', 'orden', 'total_areas', 'esta_activo']
    list_filter = ['esta_activo', 'requiere_deposito']
    search_fields = ['nombre', 'descripcion']
    ordering = ['orden', 'nombre']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def total_areas(self, obj):
        return obj.areas.count()
    total_areas.short_description = 'Total Áreas'

class ImagenAreaInline(admin.TabularInline):
    model = ImagenAreaComun
    extra = 0
    fields = ['imagen', 'titulo', 'es_portada', 'orden']

@admin.register(AreaComun)
class AdminAreaComun(admin.ModelAdmin):
    list_display = [
        'nombre', 'tipo_area', 'capacidad_maxima', 'tarifa_por_hora',
        'estado_coloreado', 'permite_reservas', 'total_reservas_admin', 'rating_promedio_admin'
    ]
    list_filter = ['tipo_area', 'estado', 'permite_reservas', 'requiere_autorizacion']
    search_fields = ['nombre', 'descripcion', 'ubicacion']
    ordering = ['tipo_area__orden', 'nombre']
    inlines = [ImagenAreaInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'tipo_area', 'ubicacion', 'imagen_principal')
        }),
        ('Capacidad y Características', {
            'fields': ('capacidad_maxima', 'area_m2')
        }),
        ('Configuración de Reservas', {
            'fields': (
                'permite_reservas', 'tiempo_minimo_reserva', 'tiempo_maximo_reserva',
                'anticipacion_minima', 'anticipacion_maxima', 'horario_funcionamiento'
            )
        }),
        ('Tarifas', {
            'fields': ('tarifa_por_hora', 'tarifa_fin_semana', 'deposito_garantia')
        }),
        ('Servicios y Permisos', {
            'fields': (
                'requiere_autorizacion', 'permite_decoracion', 'permite_musica',
                'permite_comida_externa', 'incluye_mobiliario', 'incluye_audio',
                'incluye_iluminacion'
            ),
            'classes': ('collapse',)
        }),
        ('Reglas y Equipamiento', {
            'fields': ('reglas_uso', 'equipamiento_incluido', 'restricciones_especiales'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )
    
    def estado_coloreado(self, obj):
        colores = {
            'disponible': 'green',
            'mantenimiento': 'orange',
            'inhabilitada': 'red',
            'reservada_admin': 'blue'
        }
        color = colores.get(obj.estado, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_coloreado.short_description = 'Estado'
    
    def total_reservas_admin(self, obj):
        return obj.reservas.count()
    total_reservas_admin.short_description = 'Total Reservas'
    
    def rating_promedio_admin(self, obj):
        promedio = obj.reservas.filter(calificacion__isnull=False).aggregate(
            promedio=Avg('calificacion')
        )['promedio']
        if promedio:
            return f"{promedio:.1f} ★"
        return '-'
    rating_promedio_admin.short_description = 'Rating'

class ReservaServicioInline(admin.TabularInline):
    model = ReservaServicio
    extra = 0
    fields = ['servicio', 'cantidad', 'precio_unitario', 'precio_total']
    readonly_fields = ['precio_total']

@admin.register(Reserva)
class AdminReserva(admin.ModelAdmin):
    list_display = [
        'codigo_reserva', 'area_comun', 'usuario', 'fecha_reserva',
        'hora_inicio', 'hora_fin', 'estado_coloreado', 'costo_total',
        'numero_invitados', 'calificacion_display'
    ]
    list_filter = [
        'estado', 'tipo_evento', 'area_comun__tipo_area', 'fecha_reserva',
        'requiere_aprobacion'
    ]
    search_fields = [
        'codigo_reserva', 'nombre_evento', 'usuario__email',
        'usuario__first_name', 'usuario__last_name', 'area_comun__nombre'
    ]
    date_hierarchy = 'fecha_reserva'
    ordering = ['-fecha_creacion']
    inlines = [ReservaServicioInline]
    
    fieldsets = (
        ('Información de la Reserva', {
            'fields': ('codigo_reserva', 'area_comun', 'usuario', 'unidad')
        }),
        ('Fecha y Horario', {
            'fields': ('fecha_reserva', 'hora_inicio', 'hora_fin', 'duracion_minutos')
        }),
        ('Detalles del Evento', {
            'fields': ('tipo_evento', 'nombre_evento', 'descripcion', 'numero_invitados')
        }),
        ('Servicios Requeridos', {
            'fields': (
                'requiere_decoracion', 'requiere_audio', 'requiere_iluminacion',
                'requiere_seguridad', 'requiere_limpieza_extra'
            ),
            'classes': ('collapse',)
        }),
        ('Contacto', {
            'fields': ('telefono_contacto', 'email_contacto', 'contacto_emergencia'),
            'classes': ('collapse',)
        }),
        ('Costos', {
            'fields': ('costo_base', 'costo_servicios_adicionales', 'deposito_garantia', 'costo_total')
        }),
        ('Estado y Aprobación', {
            'fields': ('estado', 'requiere_aprobacion', 'aprobado_por', 'fecha_aprobacion')
        }),
        ('Observaciones', {
            'fields': ('observaciones_usuario', 'observaciones_admin', 'motivo_cancelacion'),
            'classes': ('collapse',)
        }),
        ('Calificación', {
            'fields': ('calificacion', 'comentario_calificacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['codigo_reserva', 'duracion_minutos', 'fecha_creacion']
    
    def estado_coloreado(self, obj):
        colores = {
            'pendiente': 'orange',
            'confirmada': 'green',
            'en_uso': 'blue',
            'completada': 'darkgreen',
            'cancelada_usuario': 'red',
            'cancelada_admin': 'darkred',
            'rechazada': 'darkred'
        }
        color = colores.get(obj.estado, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_coloreado.short_description = 'Estado'
    
    def calificacion_display(self, obj):
        if obj.calificacion:
            stars = '★' * obj.calificacion + '☆' * (5 - obj.calificacion)
            return format_html('<span title="{}">{}</span>', obj.calificacion, stars)
        return '-'
    calificacion_display.short_description = 'Calificación'


@admin.register(ServicioAdicional)
class AdminServicioAdicional(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'unidad', 'esta_activo']
    list_filter = ['esta_activo', 'requiere_anticipacion']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']


@admin.register(DisponibilidadEspecial)
class AdminDisponibilidadEspecial(admin.ModelAdmin):
    list_display = ['titulo', 'area_comun', 'tipo', 'fecha_inicio', 'fecha_fin', 'esta_disponible']
    list_filter = ['tipo', 'esta_disponible', 'area_comun']
    search_fields = ['titulo', 'descripcion']
    date_hierarchy = 'fecha_inicio'
    ordering = ['-fecha_inicio']