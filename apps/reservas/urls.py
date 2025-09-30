from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    # Endpoints estándar para frontend
    path('espacios/', views.ListaAreasComunes.as_view(), name='espacios-list'),
    # path('espacios/<int:pk>/', views.DetalleAreaComun.as_view(), name='espacios-detail'),  # Vista no implementada
    path('reservas/', views.ListaReservasUsuario.as_view(), name='reservas-list'),
    # path('reservas/<int:pk>/', views.DetalleReserva.as_view(), name='reservas-detail'),  # Vista no implementada
    # Comentando temporalmente hasta implementar la función
    # path('disponibilidad/<int:espacio_id>/', views.disponibilidad_espacio, name='disponibilidad-espacio'),
    
    # Endpoints adicionales existentes
    path('tipos-areas/', views.ListaTiposAreaComun.as_view(), name='lista-tipos-areas'),
    
    # Áreas comunes - Usuario (Casos de Uso 8: Consultar disponibilidad)
    path('areas/', views.ListaAreasComunes.as_view(), name='lista-areas'),
    # path('areas/<int:pk>/', views.DetalleAreaComun.as_view(), name='detalle-area'),  # Vista no implementada
    path('disponibilidad/', views.consultar_disponibilidad, name='consultar-disponibilidad'),
    path('horarios-ocupados/', views.horarios_ocupados, name='horarios-ocupados'),
    path('calendario/', views.calendario_reservas, name='calendario-reservas'),
    
    # Áreas comunes - Administrador (Casos de Uso 15 y 16)
    path('admin/areas/', views.ListaAreasAdministrador.as_view(), name='admin-lista-areas'),
    # path('admin/areas/<int:pk>/', views.DetalleAreaAdministrador.as_view(), name='admin-detalle-area'),  # Vista no implementada
    path('admin/disponibilidad-especial/', views.crear_disponibilidad_especial, name='crear-disponibilidad-especial'),
    
    # Reservas - Usuario (Caso de Uso 6: Hacer reservas)
    path('mis-reservas/', views.ListaReservasUsuario.as_view(), name='mis-reservas'),
    # path('crear/', views.CrearReserva.as_view(), name='crear-reserva'),  # Vista no implementada
    # path('reservas/<int:pk>/', views.DetalleReserva.as_view(), name='detalle-reserva'),  # Vista no implementada
    path('reservas/<int:reserva_id>/calificar/', views.calificar_reserva, name='calificar-reserva'),
    
    # Reservas - Administrador
    path('admin/reservas/', views.ListaReservasAdministrador.as_view(), name='admin-reservas'),
    path('admin/reservas/<int:reserva_id>/aprobar/', views.aprobar_reserva, name='aprobar-reserva'),
    
    # Servicios adicionales
    path('servicios/', views.ListaServiciosAdicionales.as_view(), name='lista-servicios'),
    
    # Estadísticas
    path('estadisticas/', views.estadisticas_reservas, name='estadisticas-reservas'),
]