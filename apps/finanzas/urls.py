from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    # Unidades Habitacionales
    path('unidades/', views.ListaUnidadesHabitacionales.as_view(), name='lista-unidades'),
    path('unidades/<int:pk>/', views.DetalleUnidadHabitacional.as_view(), name='detalle-unidad'),
    
    # Tipos de Pago
    path('tipos-pago/', views.ListaTiposPago.as_view(), name='lista-tipos-pago'),
    
    # Pagos - Usuario
    path('mis-pagos/', views.ListaPagosUsuario.as_view(), name='mis-pagos'),
    path('historial/', views.historial_pagos_usuario, name='historial-usuario'),
    path('resumen/', views.resumen_financiero_usuario, name='resumen-usuario'),
    
    # Pagos - Administrador
    path('pagos/', views.ListaPagosAdmin.as_view(), name='lista-pagos-admin'),
    path('pagos/<int:pk>/', views.DetallePago.as_view(), name='detalle-pago'),
    path('pagos/<int:pago_id>/procesar/', views.procesar_pago, name='procesar-pago'),
    path('generar-pagos/', views.generar_pagos_mensuales, name='generar-pagos'),
    
    # Multas
    path('multas/', views.ListaMultas.as_view(), name='lista-multas'),
    path('multas/<int:pk>/', views.DetalleMulta.as_view(), name='detalle-multa'),
    path('aplicar-intereses/', views.aplicar_interes_moratorio, name='aplicar-intereses'),
    
    # Reportes
    path('resumen-admin/', views.resumen_financiero_admin, name='resumen-admin'),
    path('reporte-morosidad/', views.reporte_morosidad, name='reporte-morosidad'),
]