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