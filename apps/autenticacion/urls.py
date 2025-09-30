from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

app_name = 'autenticacion'

urlpatterns = [
    # JWT Authentication endpoints
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Custom authentication endpoints
    path('register/', views.RegistrarUsuario.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.VistaPerfilUsuario.as_view(), name='profile'),
    path('users/', views.ListaUsuarios.as_view(), name='users_list'),
    path('change-password/', views.CambiarPassword.as_view(), name='change_password'),
    
    # Legacy endpoints (mantener compatibilidad)
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar-sesion'),
    path('perfil/', views.VistaPerfilUsuario.as_view(), name='perfil'),
]