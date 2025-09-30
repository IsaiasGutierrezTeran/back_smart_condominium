from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Usuario, PerfilUsuario
from .serializers import SerializadorRegistroUsuario, SerializadorInicioSesion, SerializadorPerfilUsuario

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registrar_usuario(request):
    """
    Registrar un nuevo usuario en el sistema
    """
    serializador = SerializadorRegistroUsuario(data=request.data)
    if serializador.is_valid():
        usuario = serializador.save()
        refresh = RefreshToken.for_user(usuario)
        return Response({
            'mensaje': 'Usuario registrado exitosamente',
            'usuario': {
                'id': usuario.id,
                'email': usuario.email,
                'nombre_usuario': usuario.username,
                'nombre_completo': usuario.get_full_name()
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def iniciar_sesion(request):
    """
    Iniciar sesión en el sistema
    """
    serializador = SerializadorInicioSesion(data=request.data)
    if serializador.is_valid():
        usuario = serializador.validated_data['usuario']
        refresh = RefreshToken.for_user(usuario)
        return Response({
            'mensaje': 'Inicio de sesión exitoso',
            'usuario': {
                'id': usuario.id,
                'email': usuario.email,
                'nombre_usuario': usuario.username,
                'nombre_completo': usuario.get_full_name(),
                'rol': usuario.perfil.rol if hasattr(usuario, 'perfil') else 'residente'
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        })
    return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class VistaPerfilUsuario(generics.RetrieveUpdateAPIView):
    """
    Ver y actualizar perfil del usuario autenticado
    """
    serializer_class = SerializadorPerfilUsuario
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=self.request.user)
        return perfil

class RegistrarUsuario(generics.CreateAPIView):
    """
    Registrar nuevo usuario (API REST estándar)
    """
    queryset = Usuario.objects.all()
    serializer_class = SerializadorRegistroUsuario
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        refresh = RefreshToken.for_user(usuario)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED, headers=headers)

class LogoutView(generics.GenericAPIView):
    """
    Cerrar sesión y invalidar token
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"message": "Sesión cerrada exitosamente"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)

class ListaUsuarios(generics.ListAPIView):
    """
    Lista de todos los usuarios (solo para administradores)
    """
    queryset = Usuario.objects.all()
    serializer_class = SerializadorPerfilUsuario
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Solo administradores pueden ver todos los usuarios
        if self.request.user.is_superuser:
            return Usuario.objects.all()
        return Usuario.objects.filter(id=self.request.user.id)

class CambiarPassword(generics.UpdateAPIView):
    """
    Cambiar contraseña del usuario
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response(
                {"error": "Contraseña actual incorrecta"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response(
            {"message": "Contraseña actualizada exitosamente"}, 
            status=status.HTTP_200_OK
        )