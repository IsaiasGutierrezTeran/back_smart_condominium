from django.urls import path
from . import views

app_name = 'mantenimiento'

urlpatterns = [
    # Endpoints estándar para frontend - solo las vistas que existen
    path('solicitudes/', views.ListaSolicitudes.as_view(), name='solicitudes-list'),
    path('solicitudes/<int:pk>/', views.DetalleSolicitud.as_view(), name='solicitudes-detail'),
    path('tipos-solicitud/', views.ListaTiposSolicitud.as_view(), name='tipos-solicitud-list'),
    path('reportes/', views.ListaReportes.as_view(), name='reportes-list'),
    path('reportes/<int:pk>/', views.DetalleReporte.as_view(), name='reportes-detail'),
    
    # Endpoints comentados hasta implementar las vistas
    # path('tipos-solicitud/<int:pk>/', views.DetalleTipoSolicitud.as_view(), name='tipos-solicitud-detail'),
    # path('estadisticas/', views.estadisticas_mantenimiento, name='estadisticas'),
    # path('mis-solicitudes/', views.ListaSolicitudesUsuario.as_view(), name='mis-solicitudes'),
    # path('crear-solicitud/', views.CrearSolicitud.as_view(), name='crear-solicitud'),
    # path('solicitudes/<int:pk>/asignar/', views.asignar_solicitud, name='asignar-solicitud'),
    # path('solicitudes/<int:pk>/completar/', views.completar_solicitud, name='completar-solicitud'),
]