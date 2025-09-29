from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import (
    CategoriaNotificacion, Notificacion, DestinatarioNotificacion,
    AvisoGeneral, InteraccionAviso, ConfiguracionNotificacion,
    PlantillaNotificacion
)

@admin.register(CategoriaNotificacion)
class AdminCategoriaNotificacion(admin.ModelAdmin):
    list_display = ['nombre', 'prioridad', 'color_preview', 'icono', 'total_notificaciones', 'esta_activa']
    list_filter = ['prioridad', 'esta_activa']
    search_fields = ['nombre', 'descripcion']
    ordering = ['-prioridad', 'nombre']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def total_notificaciones(self, obj):
        return obj.notificaciones.count()
    total_notificaciones.short_description = 'Total Notificaciones'

class DestinatarioInline(admin.TabularInline):
    model = DestinatarioNotificacion
    extra = 0
    readonly_fields = ['fecha_envio', 'fecha_entrega', 'fecha_lectura', 'fecha_confirmacion']
    fields = ['usuario', 'estado', 'fecha_envio', 'fecha_lectura', 'dispositivo_lectura']

@admin.register(Notificacion)
class AdminNotificacion(admin.ModelAdmin):
    list_display = [
        'titulo', 'categoria', 'tipo_destinatario', 'estado_coloreado', 
        'es_urgente', 'total_destinatarios', 'total_leidos', 'tasa_apertura_display',
        'fecha_creacion', 'creado_por'
    ]
    list_filter = ['estado', 'categoria', 'tipo_destinatario', 'es_urgente', 'fecha_creacion']
    search_fields = ['titulo', 'mensaje', 'creado_por__email']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']
    inlines = [DestinatarioInline]
    
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'mensaje', 'categoria')
        }),
        ('Destinatarios', {
            'fields': ('tipo_destinatario', 'edificios_objetivo', 'unidades_objetivo')
        }),
        ('Configuración de Envío', {
            'fields': ('es_push', 'es_email', 'es_sms', 'es_urgente', 'requiere_confirmacion')
        }),
        ('Programación', {
            'fields': ('enviar_inmediatamente', 'fecha_programada', 'fecha_expiracion')
        }),
        ('Archivos', {
            'fields': ('imagen', 'archivo_adjunto'),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('estado', 'total_destinatarios', 'total_enviados', 'total_leidos', 'total_confirmados'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['total_destinatarios', 'total_enviados', 'total_leidos', 'total_confirmados']
    
    def estado_coloreado(self, obj):
        colores = {
            'borrador': 'gray',
            'programada': 'orange',
            'enviada': 'green',
            'cancelada': 'red'
        }
        color = colores.get(obj.estado, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_coloreado.short_description = 'Estado'
    
    def tasa_apertura_display(self, obj):
        if obj.total_enviados > 0:
            tasa = obj.tasa_apertura
            color = 'green' if tasa >= 70 else 'orange' if tasa >= 40 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
                color, tasa
            )
        return '-'
    tasa_apertura_display.short_description = 'Tasa Apertura'

@admin.register(DestinatarioNotificacion)
class AdminDestinatarioNotificacion(admin.ModelAdmin):
    list_display = [
        'notificacion_titulo', 'usuario', 'estado', 'fecha_envio', 
        'fecha_lectura', 'dispositivo_lectura'
    ]
    list_filter = ['estado', 'dispositivo_lectura', 'fecha_envio']
    search_fields = ['notificacion__titulo', 'usuario__email', 'usuario__first_name']
    date_hierarchy = 'fecha_envio'
    ordering = ['-fecha_envio']
    
    def notificacion_titulo(self, obj):
        return obj.notificacion.titulo[:50] + "..." if len(obj.notificacion.titulo) > 50 else obj.notificacion.titulo
    notificacion_titulo.short_description = 'Notificación'

@admin.register(AvisoGeneral)
class AdminAvisoGeneral(admin.ModelAdmin):
    list_display = [
        'titulo', 'tipo_aviso', 'es_destacado', 'dirigido_a', 
        'visualizaciones', 'likes', 'esta_vigente_display', 'fecha_creacion'
    ]
    list_filter = ['tipo_aviso', 'es_destacado', 'dirigido_a', 'esta_activo']
    search_fields = ['titulo', 'contenido']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-es_destacado', '-fecha_creacion']
    
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'contenido', 'tipo_aviso')
        }),
        ('Configuración', {
            'fields': ('es_destacado', 'mostrar_en_inicio', 'requiere_notificacion')
        }),
        ('Destinatarios', {
            'fields': ('dirigido_a', 'edificios_objetivo')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Archivos', {
            'fields': ('imagen_portada', 'archivo_adjunto'),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('visualizaciones', 'likes'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['visualizaciones', 'likes']
    
    def esta_vigente_display(self, obj):
        if obj.esta_vigente:
            return format_html('<span style="color: green;">✓ Vigente</span>')
        return format_html('<span style="color: red;">✗ No Vigente</span>')
    esta_vigente_display.short_description = 'Vigente'

@admin.register(ConfiguracionNotificacion)
class AdminConfiguracionNotificacion(admin.ModelAdmin):
    list_display = [
        'usuario', 'recibir_push', 'recibir_email', 'recibir_sms',
        'horario_inicio', 'horario_fin', 'no_molestar_fines_semana'
    ]
    list_filter = ['recibir_push', 'recibir_email', 'recibir_sms', 'no_molestar_fines_semana']
    search_fields = ['usuario__email', 'usuario__first_name', 'usuario__last_name']
    ordering = ['usuario__email']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('usuario',)
        }),
        ('Canales de Notificación', {
            'fields': ('recibir_push', 'recibir_email', 'recibir_sms')
        }),
        ('Tipos de Notificación', {
            'fields': (
                'notif_pagos', 'notif_mantenimiento', 'notif_seguridad',
                'notif_eventos', 'notif_avisos', 'notif_reservas'
            )
        }),
        ('Configuración de Horario', {
            'fields': ('horario_inicio', 'horario_fin', 'no_molestar_fines_semana')
        }),
        ('Tokens FCM', {
            'fields': ('token_fcm_android', 'token_fcm_ios', 'token_fcm_web'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PlantillaNotificacion)
class AdminPlantillaNotificacion(admin.ModelAdmin):
    list_display = [
        'nombre', 'categoria_default', 'es_sistema', 'esta_activa', 
        'uso_contador', 'fecha_creacion'
    ]
    list_filter = ['es_sistema', 'esta_activa', 'categoria_default']
    search_fields = ['nombre', 'descripcion', 'titulo_plantilla']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Contenido de la Plantilla', {
            'fields': ('titulo_plantilla', 'mensaje_plantilla', 'variables_disponibles')
        }),
        ('Configuración por Defecto', {
            'fields': ('categoria_default', 'es_push_default', 'es_email_default')
        }),
        ('Estado', {
            'fields': ('es_sistema', 'esta_activa', 'uso_contador')
        }),
    )
    
    readonly_fields = ['uso_contador']