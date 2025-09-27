from django.urls import path
from . import views

app_name = 'autenticacion'

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar-sesion'),
    path('perfil/', views.VistaPerfilUsuario.as_view(), name='perfil'),
]