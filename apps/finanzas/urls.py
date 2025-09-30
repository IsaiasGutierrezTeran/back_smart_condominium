from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    # Endpoints estándar para frontend
    path('cuotas/', views.ListaCuotas.as_view(), name='cuotas-list'),
    path('cuotas/<int:pk>/', views.DetalleCuota.as_view(), name='cuotas-detail'),
    path('pagos/', views.ListaPagos.as_view(), name='pagos-list'),
    path('pagos/<int:pk>/', views.DetallePago.as_view(), name='pagos-detail'),
    path('gastos/', views.ListaGastos.as_view(), name='gastos-list'),
    path('gastos/<int:pk>/', views.DetalleGasto.as_view(), name='gastos-detail'),
    path('reporte-financiero/', views.reporte_financiero, name='reporte-financiero'),
    path('estadisticas-pagos/', views.estadisticas_pagos, name='estadisticas-pagos'),
    
    # Endpoints adicionales existentes
    path('unidades/', views.ListaUnidadesHabitacionales.as_view(), name='lista-unidades'),
    path('unidades/<int:pk>/', views.DetalleUnidadHabitacional.as_view(), name='detalle-unidad'),
    path('tipos-pago/', views.ListaTiposPago.as_view(), name='lista-tipos-pago'),
    path('mis-pagos/', views.ListaPagosUsuario.as_view(), name='mis-pagos'),
    path('historial/', views.historial_pagos_usuario, name='historial-usuario'),
    path('resumen/', views.resumen_financiero_usuario, name='resumen-usuario'),
    path('pagos/<int:pago_id>/procesar/', views.procesar_pago, name='procesar-pago'),
    path('generar-pagos/', views.generar_pagos_mensuales, name='generar-pagos'),
    path('multas/', views.ListaMultas.as_view(), name='lista-multas'),
    path('multas/<int:pk>/', views.DetalleMulta.as_view(), name='detalle-multa'),
    path('aplicar-intereses/', views.aplicar_interes_moratorio, name='aplicar-intereses'),
    path('resumen-admin/', views.resumen_financiero_admin, name='resumen-admin'),
    path('reporte-morosidad/', views.reporte_morosidad, name='reporte-morosidad'),
]