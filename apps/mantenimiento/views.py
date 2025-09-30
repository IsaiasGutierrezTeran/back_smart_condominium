from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import SolicitudMantenimiento, TipoSolicitud, ReporteMantenimiento
from apps.autenticacion.models import Usuario

class ListaSolicitudes(generics.ListCreateAPIView):
    """
    Listar y crear solicitudes de mantenimiento
    """
    queryset = SolicitudMantenimiento.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - necesita implementar serializers
        from rest_framework import serializers
        class SolicitudSerializer(serializers.ModelSerializer):
            class Meta:
                model = SolicitudMantenimiento
                fields = '__all__'
        return SolicitudSerializer
    
    def get_queryset(self):
        queryset = SolicitudMantenimiento.objects.all()
        # Filtrar por usuario si no es admin
        if not self.request.user.is_staff:
            queryset = queryset.filter(solicitante=self.request.user)
        return queryset.order_by('-fecha_solicitud')

class DetalleSolicitud(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar solicitud de mantenimiento
    """
    queryset = SolicitudMantenimiento.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - necesita implementar serializers
        from rest_framework import serializers
        class SolicitudSerializer(serializers.ModelSerializer):
            class Meta:
                model = SolicitudMantenimiento
                fields = '__all__'
        return SolicitudSerializer

class ListaTiposSolicitud(generics.ListCreateAPIView):
    """
    Listar y crear tipos de solicitud
    """
    queryset = TipoSolicitud.objects.filter(esta_activo=True)
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - necesita implementar serializers
        from rest_framework import serializers
        class TipoSolicitudSerializer(serializers.ModelSerializer):
            class Meta:
                model = TipoSolicitud
                fields = '__all__'
        return TipoSolicitudSerializer
    
    def perform_create(self, serializer):
        # Solo administradores pueden crear tipos
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Solo administradores pueden crear tipos de solicitud")
        serializer.save()

class ListaReportes(generics.ListCreateAPIView):
    """
    Listar y crear reportes de mantenimiento
    """
    queryset = ReporteMantenimiento.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - necesita implementar serializers
        from rest_framework import serializers
        class ReporteSerializer(serializers.ModelSerializer):
            class Meta:
                model = ReporteMantenimiento
                fields = '__all__'
        return ReporteSerializer
    
    def get_queryset(self):
        queryset = ReporteMantenimiento.objects.all()
        # Solo administradores pueden ver todos los reportes
        if not self.request.user.is_staff:
            return queryset.none()
        return queryset.order_by('-fecha_creacion')

class DetalleReporte(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar reporte de mantenimiento
    """
    queryset = ReporteMantenimiento.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - necesita implementar serializers
        from rest_framework import serializers
        class ReporteSerializer(serializers.ModelSerializer):
            class Meta:
                model = ReporteMantenimiento
                fields = '__all__'
        return ReporteSerializer
