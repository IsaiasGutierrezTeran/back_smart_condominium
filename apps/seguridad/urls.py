from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# URLs para la app de seguridad con IA
urlpatterns = [
    # Tipos de visitantes
    path('tipos-visitantes/', views.TipoVisitanteListCreateView.as_view(), name='tipos-visitantes-list'),
    path('tipos-visitantes/<int:pk>/', views.TipoVisitanteDetailView.as_view(), name='tipos-visitantes-detail'),
    
    # Registro de visitantes
    path('visitantes/', views.RegistroVisitanteListCreateView.as_view(), name='visitantes-list'),
    path('visitantes/<int:pk>/', views.RegistroVisitanteDetailView.as_view(), name='visitantes-detail'),
    
    # Reconocimiento facial
    path('reconocimiento-facial/', views.reconocimiento_facial, name='reconocimiento-facial'),
    
    # Control vehicular
    path('vehiculos/', views.AccesoVehiculoListCreateView.as_view(), name='vehiculos-list'),
    path('vehiculos/<int:pk>/', views.AccesoVehiculoDetailView.as_view(), name='vehiculos-detail'),
    
    # OCR de placas
    path('ocr-placa/', views.ocr_placa_vehicular, name='ocr-placa'),
    
    # Registro de accesos
    path('accesos/', views.RegistroAccesoListCreateView.as_view(), name='accesos-list'),
    path('accesos/<int:pk>/', views.RegistroAccesoDetailView.as_view(), name='accesos-detail'),
    
    # Incidentes de seguridad
    path('incidentes/', views.IncidenteSeguridadListCreateView.as_view(), name='incidentes-list'),
    path('incidentes/<int:pk>/', views.IncidenteSeguridadDetailView.as_view(), name='incidentes-detail'),
    
    # Detección de anomalías
    path('detectar-anomalias/', views.detectar_anomalias, name='detectar-anomalias'),
    
    # Configuración de IA
    path('configuracion-ia/', views.ConfiguracionIAListCreateView.as_view(), name='configuracion-ia-list'),
    path('configuracion-ia/<int:pk>/', views.ConfiguracionIADetailView.as_view(), name='configuracion-ia-detail'),
    
    # Análisis predictivo de morosidad
    path('analisis-morosidad/', views.AnalisisPredictivoMorosidadListView.as_view(), name='analisis-morosidad-list'),
    path('generar-analisis-morosidad/', views.generar_analisis_morosidad, name='generar-analisis-morosidad'),
    
    # Dashboard y reportes
    path('dashboard/', views.dashboard_seguridad, name='dashboard-seguridad'),
    path('reporte-periodo/', views.reporte_seguridad_periodo, name='reporte-periodo'),
]