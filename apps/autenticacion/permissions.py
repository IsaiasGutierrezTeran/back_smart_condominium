from rest_framework import permissions

class IsAdministrador(permissions.BasePermission):
    """
    Permiso para administradores únicamente
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.tipo_usuario == 'administrador' or request.user.is_superuser

class IsResidente(permissions.BasePermission):
    """
    Permiso para residentes únicamente
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.tipo_usuario == 'residente'

class IsSeguridad(permissions.BasePermission):
    """
    Permiso para personal de seguridad únicamente
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.tipo_usuario == 'seguridad'

class IsAdministradorOrSeguridad(permissions.BasePermission):
    """
    Permiso para administradores o personal de seguridad
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (request.user.tipo_usuario in ['administrador', 'seguridad'] or 
                request.user.is_superuser)

class IsAdministradorOrResidente(permissions.BasePermission):
    """
    Permiso para administradores o residentes
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (request.user.tipo_usuario in ['administrador', 'residente'] or 
                request.user.is_superuser)

class IsOwnerOrAdministrador(permissions.BasePermission):
    """
    Permiso para propietarios del objeto o administradores
    """
    def has_object_permission(self, request, view, obj):
        # Administradores tienen acceso completo
        if request.user.tipo_usuario == 'administrador' or request.user.is_superuser:
            return True
        
        # Verificar si el usuario es propietario del objeto
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        elif hasattr(obj, 'propietario'):
            return obj.propietario == request.user
        elif hasattr(obj, 'creado_por'):
            return obj.creado_por == request.user
        
        return False

class IsReadOnlyOrAdministrador(permissions.BasePermission):
    """
    Permiso de solo lectura para todos, escritura solo para administradores
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Lectura permitida para todos los usuarios autenticados
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Escritura solo para administradores
        return (request.user.tipo_usuario == 'administrador' or 
                request.user.is_superuser)