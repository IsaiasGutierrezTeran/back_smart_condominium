from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, PerfilUsuario

class SerializadorRegistroUsuario(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, label="Contraseña")
    confirmar_password = serializers.CharField(write_only=True, label="Confirmar Contraseña")
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'confirmar_password', 
                 'first_name', 'last_name', 'telefono']
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'telefono': 'Teléfono'
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirmar_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirmar_password')
        password = validated_data.pop('password')
        usuario = Usuario.objects.create_user(**validated_data)
        usuario.set_password(password)
        usuario.save()
        
        # Crear perfil por defecto
        PerfilUsuario.objects.create(usuario=usuario)
        return usuario

class SerializadorInicioSesion(serializers.Serializer):
    email = serializers.EmailField(label="Correo Electrónico")
    password = serializers.CharField(label="Contraseña")
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            usuario = authenticate(username=email, password=password)
            if not usuario:
                raise serializers.ValidationError('Credenciales inválidas')
            if not usuario.is_active:
                raise serializers.ValidationError('Cuenta desactivada')
            attrs['usuario'] = usuario
        return attrs

class SerializadorPerfilUsuario(serializers.ModelSerializer):
    email_usuario = serializers.EmailField(source='usuario.email', read_only=True, label="Correo")
    nombre_usuario = serializers.CharField(source='usuario.get_full_name', read_only=True, label="Nombre Completo")
    
    class Meta:
        model = PerfilUsuario
        fields = '__all__'
        labels = {
            'rol': 'Rol',
            'numero_unidad': 'Número de Unidad',
            'edificio': 'Edificio',
            'avatar': 'Foto de Perfil',
            'contacto_emergencia': 'Contacto de Emergencia',
            'es_propietario': 'Es Propietario'
        }