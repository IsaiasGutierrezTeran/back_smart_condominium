from django.urls import path
from . import views

app_name = 'comunicacion'

urlpatterns = [
    # Categorías
    path('categorias/', views.ListaCategorias.as_view(), name='lista-categorias'),
    path('categorias/<int:pk>/', views.DetalleCategoria.as_view(), name='detalle-categoria'),
    
    # Notificaciones - Administrador
    path('notificaciones/', views.ListaNotificacionesAdmin.as_view(), name='lista-notificaciones-admin'),
    path('notificaciones/<int:pk>/', views.DetalleNotificacion.as_view(), name='detalle-notificacion'),
    path('notificaciones/<int:notificacion_id>/enviar/', views.enviar_notificacion, name='enviar-notificacion'),
    path('notificacion-masiva/', views.notificacion_masiva, name='notificacion-masiva'),
    
    # Notificaciones - Usuario
    path('mis-notificaciones/', views.mis_notificaciones, name='mis-notificaciones'),
    path('marcar-leida/<int:notificacion_id>/', views.marcar_como_leida, name='marcar-leida'),
    path('confirmar/<int:notificacion_id>/', views.confirmar_notificacion, name='confirmar-notificacion'),
    path('estadisticas/', views.estadisticas_notificaciones, name='estadisticas-notificaciones'),
    
    # Avisos Generales
    path('avisos/', views.ListaAvisosGenerales.as_view(), name='lista-avisos'),
    path('avisos/<int:pk>/', views.DetalleAvisoGeneral.as_view(), name='detalle-aviso'),
    path('avisos/<int:aviso_id>/interactuar/', views.interactuar_aviso, name='interactuar-aviso'),
    
    # Configuración
    path('configuracion/', views.ConfiguracionNotificacionUsuario.as_view(), name='configuracion-notificaciones'),
    path('actualizar-token-fcm/', views.actualizar_token_fcm, name='actualizar-token-fcm'),
    
    # Plantillas
    path('plantillas/', views.ListaPlantillas.as_view(), name='lista-plantillas'),
    path('renderizar-plantilla/', views.renderizar_plantilla, name='renderizar-plantilla'),
]