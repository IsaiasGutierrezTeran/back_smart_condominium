from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    TipoVisitante, RegistroVisitante, AccesoVehiculo, RegistroAcceso,
    IncidenteSeguridad, ConfiguracionIA, AnalisisPredictivoMorosidad
)

@admin.register(TipoVisitante)
class TipoVisitanteAdmin(admin.ModelAdmin):
    """Administración de tipos de visitantes"""
    list_display = ['nombre', 'requiere_autorizacion', 'tiempo_maximo_visita', 'color_display', 'esta_activo']
    list_filter = ['requiere_autorizacion', 'esta_activo']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['esta_activo']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'esta_activo')
        }),
        ('Configuración', {
            'fields': ('requiere_autorizacion', 'tiempo_maximo_visita')
        }),
        ('Apariencia', {
            'fields': ('color', 'icono')
        }),
    )
    
    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'

@admin.register(RegistroVisitante)
class RegistroVisitanteAdmin(admin.ModelAdmin):
    """Administración de registro de visitantes"""
    list_display = [
        'nombre_completo', 'documento_identidad', 'tipo_visitante', 
        'unidad_destino', 'estado', 'fecha_ingreso', 'metodo_identificacion'
    ]
    list_filter = [
        'estado', 'tipo_visitante', 'metodo_identificacion', 
        'fecha_creacion', 'fecha_ingreso'
    ]
    search_fields = [
        'nombres', 'apellidos', 'documento_identidad', 
        'telefono', 'motivo_visita'
    ]
    list_editable = ['estado']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombres', 'apellidos', 'documento_identidad', 'telefono')
        }),
        ('Información de Visita', {
            'fields': ('tipo_visitante', 'unidad_destino', 'motivo_visita', 'estado')
        }),
        ('Autorización', {
            'fields': ('autorizado_por', 'fecha_autorizacion')
        }),
        ('Control de Tiempo', {
            'fields': ('fecha_ingreso', 'fecha_salida')
        }),
        ('Reconocimiento Facial', {
            'fields': ('foto_ingreso', 'foto_salida', 'metodo_identificacion', 
                      'confianza_reconocimiento', 'datos_faciales_json'),
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': ('codigo_qr', 'observaciones'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['codigo_qr', 'fecha_creacion', 'fecha_actualizacion', 'registrado_por']
    
    def save_model(self, request, obj, form, change):
        """Asignar automáticamente el usuario que está registrando"""
        if not change:  # Solo para nuevos objetos
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)
    
    def nombre_completo(self, obj):
        return obj.nombre_completo
    nombre_completo.short_description = 'Nombre Completo'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'tipo_visitante', 'unidad_destino', 'autorizado_por', 'registrado_por'
        )

@admin.register(AccesoVehiculo)
class AccesoVehiculoAdmin(admin.ModelAdmin):
    """Administración de acceso vehicular"""
    list_display = [
        'placa_vehiculo', 'tipo_vehiculo', 'marca_modelo', 
        'propietario', 'unidad_asignada', 'estado_acceso'
    ]
    list_filter = [
        'tipo_vehiculo', 'estado_acceso', 'fecha_creacion'
    ]
    search_fields = [
        'placa_vehiculo', 'marca', 'modelo', 'color',
        'propietario__first_name', 'propietario__last_name'
    ]
    list_editable = ['estado_acceso']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']
    
    fieldsets = (
        ('Información del Vehículo', {
            'fields': ('placa_vehiculo', 'tipo_vehiculo', 'marca', 'modelo', 'color', 'año')
        }),
        ('Propietario y Ubicación', {
            'fields': ('propietario', 'unidad_asignada')
        }),
        ('Control de Acceso', {
            'fields': ('estado_acceso', 'fecha_inicio_acceso', 'fecha_fin_acceso')
        }),
        ('OCR y Reconocimiento', {
            'fields': ('foto_vehiculo', 'confianza_ocr', 'datos_ocr_json'),
            'classes': ('collapse',)
        }),
        ('Información Adicional', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'registrado_por']
    
    def save_model(self, request, obj, form, change):
        """Asignar automáticamente el usuario que está registrando"""
        if not change:  # Solo para nuevos objetos
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)
    
    def marca_modelo(self, obj):
        return f"{obj.marca} {obj.modelo}" if obj.marca and obj.modelo else obj.marca or obj.modelo or '-'
    marca_modelo.short_description = 'Marca/Modelo'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'propietario', 'unidad_asignada', 'registrado_por'
        )

@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    """Administración de registro de accesos"""
    list_display = [
        'fecha_hora', 'tipo_acceso', 'metodo_acceso', 'usuario',
        'ubicacion', 'exitoso'
    ]
    list_filter = [
        'tipo_acceso', 'metodo_acceso', 'exitoso', 'fecha_hora'
    ]
    search_fields = [
        'usuario__first_name', 'usuario__last_name', 'usuario__email',
        'ubicacion'
    ]
    date_hierarchy = 'fecha_hora'
    ordering = ['-fecha_hora']
    
    fieldsets = (
        ('Información del Acceso', {
            'fields': ('tipo_acceso', 'metodo_acceso', 'ubicacion')
        }),
        ('Usuario', {
            'fields': ('usuario',)
        }),
        ('Control y Seguridad', {
            'fields': ('exitoso', 'observaciones')
        }),
        ('Datos Biométricos', {
            'fields': ('foto_acceso', 'datos_biometricos'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_hora']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario')

@admin.register(IncidenteSeguridad)
class IncidenteSeguridadAdmin(admin.ModelAdmin):
    """Administración de incidentes de seguridad"""
    list_display = [
        'titulo', 'tipo_incidente', 'nivel_gravedad',
        'estado', 'fecha_incidente', 'reportado_por'
    ]
    list_filter = [
        'tipo_incidente', 'nivel_gravedad', 'estado', 'fecha_incidente'
    ]
    search_fields = [
        'titulo', 'descripcion', 'ubicacion',
        'reportado_por__first_name', 'reportado_por__last_name'
    ]
    list_editable = ['estado']
    date_hierarchy = 'fecha_incidente'
    ordering = ['-fecha_incidente']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'tipo_incidente', 'nivel_gravedad')
        }),
        ('Ubicación y Tiempo', {
            'fields': ('ubicacion', 'fecha_incidente')
        }),
        ('Evidencia', {
            'fields': ('evidencia_foto',),
            'classes': ('collapse',)
        }),
        ('Gestión', {
            'fields': ('estado', 'reportado_por', 'resuelto_por', 'fecha_resolucion')
        }),
        ('Resolución', {
            'fields': ('resolucion',),
            'classes': ('collapse',)
        }),
        ('Datos de IA', {
            'fields': ('datos_ia_json',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'reportado_por', 'resuelto_por', 'unidad_afectada'
        )

@admin.register(ConfiguracionIA)
class ConfiguracionIAAdmin(admin.ModelAdmin):
    """Administración de configuración de IA"""
    list_display = [
        'nombre', 'tipo_algoritmo', 'version_modelo', 'esta_activo',
        'umbral_confianza', 'precision_promedio', 'fecha_ultima_actualizacion'
    ]
    list_filter = [
        'tipo_algoritmo', 'esta_activo', 'generar_alertas',
        'fecha_creacion', 'fecha_ultima_actualizacion'
    ]
    search_fields = ['nombre', 'descripcion', 'modelo_ia']
    list_editable = ['esta_activo', 'umbral_confianza']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo_algoritmo', 'descripcion', 'esta_activo')
        }),
        ('Configuración Técnica', {
            'fields': ('modelo_ia', 'version_modelo', 'parametros_configuracion', 'umbral_confianza')
        }),
        ('Métricas de Rendimiento', {
            'fields': ('precision_promedio', 'recall_promedio', 'tiempo_procesamiento_ms'),
            'classes': ('collapse',)
        }),
        ('Alertas', {
            'fields': ('generar_alertas', 'nivel_alerta_minimo'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_ultima_actualizacion', 'creado_por']
    
    def save_model(self, request, obj, form, change):
        """Asignar automáticamente el usuario que está creando la configuración"""
        if not change:  # Solo para nuevos objetos
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('creado_por')

@admin.register(AnalisisPredictivoMorosidad)
class AnalisisPredictivoMorosidadAdmin(admin.ModelAdmin):
    """Administración de análisis predictivo de morosidad"""
    list_display = [
        'unidad', 'usuario_analizado', 'nivel_riesgo', 'probabilidad_morosidad',
        'confianza_prediccion', 'fecha_analisis', 'valido_hasta', 'fue_preciso'
    ]
    list_filter = [
        'nivel_riesgo', 'fue_preciso', 'fecha_analisis', 'valido_hasta'
    ]
    search_fields = [
        'unidad__numero_unidad', 'usuario_analizado__first_name',
        'usuario_analizado__last_name', 'usuario_analizado__email'
    ]
    date_hierarchy = 'fecha_analisis'
    ordering = ['-fecha_analisis']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('unidad', 'usuario_analizado', 'fecha_analisis')
        }),
        ('Resultados del Análisis', {
            'fields': ('probabilidad_morosidad', 'nivel_riesgo', 'confianza_prediccion')
        }),
        ('Factores y Recomendaciones', {
            'fields': ('factores_riesgo', 'recomendaciones', 'acciones_sugeridas'),
            'classes': ('collapse',)
        }),
        ('Datos Técnicos', {
            'fields': ('modelo_utilizado', 'version_modelo', 'historial_pagos_analizado'),
            'classes': ('collapse',)
        }),
        ('Seguimiento', {
            'fields': ('valido_hasta', 'fue_preciso'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_analisis', 'generado_por']
    
    def save_model(self, request, obj, form, change):
        """Asignar automáticamente el usuario que está generando el análisis"""
        if not change:  # Solo para nuevos objetos
            obj.generado_por = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'unidad', 'usuario_analizado', 'generado_por'
        )

# Configuración del sitio de administración
admin.site.site_header = "Smart Condominium - Módulo de Seguridad"
admin.site.site_title = "Seguridad Admin"
admin.site.index_title = "Administración de Seguridad con IA"
