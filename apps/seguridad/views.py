from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta
import json
import base64
import uuid
from io import BytesIO

from .models import (
    TipoVisitante, RegistroVisitante, AccesoVehiculo, RegistroAcceso,
    IncidenteSeguridad, ConfiguracionIA, AnalisisPredictivoMorosidad
)
from .serializers import (
    TipoVisitanteSerializer, RegistroVisitanteSerializer, RegistroVisitanteListSerializer,
    AccesoVehiculoSerializer, AccesoVehiculoListSerializer, RegistroAccesoSerializer,
    IncidenteSeguridadSerializer, IncidenteSeguridadListSerializer,
    ConfiguracionIASerializer, AnalisisPredictivoMorosidadSerializer,
    ReconocimientoFacialSerializer, OCRPlacaSerializer, DeteccionAnomaliaSerializer,
    AnalisisMorosidadSerializer
)
from apps.autenticacion.permissions import IsAdministradorOrSeguridad
from apps.finanzas.models import UnidadHabitacional, Pago

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# =====================================================================
# TIPOS DE VISITANTES
# =====================================================================

class TipoVisitanteListCreateView(generics.ListCreateAPIView):
    """
    Lista y crea tipos de visitantes
    """
    queryset = TipoVisitante.objects.filter(esta_activo=True)
    serializer_class = TipoVisitanteSerializer
    permission_classes = [IsAuthenticated, IsAdministradorOrSeguridad]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']
    ordering = ['nombre']

class TipoVisitanteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualiza y elimina tipos de visitantes
    """
    queryset = TipoVisitante.objects.all()
    serializer_class = TipoVisitanteSerializer
    permission_classes = [IsAuthenticated, IsAdministradorOrSeguridad]
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.esta_activo = False
        instance.save()

# =====================================================================
# REGISTRO DE VISITANTES CON IA
# =====================================================================

class RegistroVisitanteListCreateView(generics.ListCreateAPIView):
    """
    Lista y crea registros de visitantes con reconocimiento facial
    """
    serializer_class = RegistroVisitanteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['estado', 'tipo_visitante', 'unidad_destino']
    search_fields = ['nombres', 'apellidos', 'documento_identidad', 'motivo_visita']
    ordering_fields = ['fecha_creacion', 'fecha_ingreso', 'nombres']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        queryset = RegistroVisitante.objects.select_related(
            'tipo_visitante', 'unidad_destino', 'autorizado_por', 'registrado_por'
        )
        
        # Filtros por fecha
        fecha_desde = self.request.query_params.get('fecha_desde')
        fecha_hasta = self.request.query_params.get('fecha_hasta')
        
        if fecha_desde:
            queryset = queryset.filter(fecha_creacion__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_creacion__lte=fecha_hasta)
        
        # Filtro por visitantes activos
        solo_activos = self.request.query_params.get('solo_activos')
        if solo_activos == 'true':
            queryset = queryset.filter(estado__in=['autorizado', 'en_visita'])
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RegistroVisitanteListSerializer
        return RegistroVisitanteSerializer
    
    def perform_create(self, serializer):
        serializer.save(registrado_por=self.request.user)

class RegistroVisitanteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualiza y elimina registros de visitantes
    """
    queryset = RegistroVisitante.objects.select_related(
        'tipo_visitante', 'unidad_destino', 'autorizado_por', 'registrado_por'
    )
    serializer_class = RegistroVisitanteSerializer
    permission_classes = [IsAuthenticated]

# =====================================================================
# RECONOCIMIENTO FACIAL
# =====================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reconocimiento_facial(request):
    """
    Endpoint para reconocimiento facial de visitantes
    """
    serializer = ReconocimientoFacialSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    imagen = serializer.validated_data['imagen']
    confianza_minima = serializer.validated_data['confianza_minima']
    incluir_biometricos = serializer.validated_data['incluir_datos_biometricos']
    
    try:
        # Simular procesamiento de IA (aquí integrarías con un servicio real de IA)
        resultado_ia = procesar_reconocimiento_facial(imagen, confianza_minima)
        
        # Buscar visitante en base de datos
        visitante_encontrado = None
        if resultado_ia['persona_identificada']:
            # Buscar por datos biométricos similares
            visitantes_candidatos = RegistroVisitante.objects.filter(
                datos_faciales_json__isnull=False
            )
            
            for visitante in visitantes_candidatos:
                similitud = calcular_similitud_facial(
                    resultado_ia['datos_faciales'],
                    visitante.datos_faciales_json
                )
                if similitud >= float(confianza_minima):
                    visitante_encontrado = visitante
                    break
        
        response_data = {
            'success': True,
            'persona_identificada': resultado_ia['persona_identificada'],
            'confianza': resultado_ia['confianza'],
            'visitante_registrado': visitante_encontrado is not None,
            'datos_faciales': resultado_ia['datos_faciales'] if incluir_biometricos else None
        }
        
        if visitante_encontrado:
            response_data['visitante'] = RegistroVisitanteSerializer(
                visitante_encontrado, context={'request': request}
            ).data
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Error en el procesamiento de reconocimiento facial',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def procesar_reconocimiento_facial(imagen, confianza_minima):
    """
    Simula el procesamiento de reconocimiento facial
    En producción, aquí integrarías con servicios como AWS Rekognition, 
    Azure Face API, o modelos locales como face_recognition
    """
    # Simular procesamiento
    import random
    
    confianza = random.uniform(60.0, 95.0)
    persona_identificada = confianza >= float(confianza_minima)
    
    datos_faciales = {
        'face_encoding': [random.uniform(-1, 1) for _ in range(128)],  # Simulado
        'face_landmarks': {
            'left_eye': [(random.randint(50, 150), random.randint(50, 100)) for _ in range(6)],
            'right_eye': [(random.randint(200, 300), random.randint(50, 100)) for _ in range(6)],
            'nose': [(random.randint(150, 200), random.randint(100, 150)) for _ in range(4)],
            'mouth': [(random.randint(120, 230), random.randint(180, 220)) for _ in range(8)]
        },
        'face_bbox': [random.randint(50, 100), random.randint(50, 100), 
                     random.randint(200, 300), random.randint(200, 300)],
        'processed_at': timezone.now().isoformat()
    }
    
    return {
        'persona_identificada': persona_identificada,
        'confianza': round(confianza, 2),
        'datos_faciales': datos_faciales
    }

def calcular_similitud_facial(datos1, datos2):
    """
    Simula el cálculo de similitud entre dos conjuntos de datos faciales
    """
    # En producción usarías algoritmos reales de comparación facial
    import random
    return random.uniform(70.0, 95.0)

# =====================================================================
# CONTROL DE ACCESO VEHICULAR
# =====================================================================

class AccesoVehiculoListCreateView(generics.ListCreateAPIView):
    """
    Lista y registra vehículos con OCR de placas
    """
    serializer_class = AccesoVehiculoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['tipo_vehiculo', 'estado_acceso', 'es_vehiculo_residente']
    search_fields = ['placa_vehiculo', 'marca', 'modelo', 'propietario__first_name', 'propietario__last_name']
    ordering_fields = ['fecha_creacion', 'placa_vehiculo']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        queryset = AccesoVehiculo.objects.select_related(
            'propietario', 'unidad_asignada', 'registrado_por'
        ).filter(esta_activo=True)
        
        # Filtro por unidad
        unidad_id = self.request.query_params.get('unidad')
        if unidad_id:
            queryset = queryset.filter(unidad_asignada_id=unidad_id)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AccesoVehiculoListSerializer
        return AccesoVehiculoSerializer
    
    def perform_create(self, serializer):
        serializer.save(registrado_por=self.request.user)

class AccesoVehiculoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualiza y elimina registros de vehículos
    """
    queryset = AccesoVehiculo.objects.select_related(
        'propietario', 'unidad_asignada', 'registrado_por'
    )
    serializer_class = AccesoVehiculoSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.esta_activo = False
        instance.save()

# =====================================================================
# OCR DE PLACAS VEHICULARES
# =====================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ocr_placa_vehicular(request):
    """
    Endpoint para OCR de placas vehiculares
    """
    serializer = OCRPlacaSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    imagen = serializer.validated_data['imagen']
    confianza_minima = serializer.validated_data['confianza_minima']
    pais_formato = serializer.validated_data['pais_formato']
    
    try:
        # Procesar OCR (simular integración con servicios de IA)
        resultado_ocr = procesar_ocr_placa(imagen, confianza_minima, pais_formato)
        
        # Buscar vehículo en base de datos
        vehiculo_encontrado = None
        if resultado_ocr['placa_detectada']:
            try:
                vehiculo_encontrado = AccesoVehiculo.objects.get(
                    placa_vehiculo=resultado_ocr['placa_texto'],
                    esta_activo=True
                )
            except AccesoVehiculo.DoesNotExist:
                pass
        
        response_data = {
            'success': True,
            'placa_detectada': resultado_ocr['placa_detectada'],
            'placa_texto': resultado_ocr['placa_texto'],
            'confianza': resultado_ocr['confianza'],
            'vehiculo_registrado': vehiculo_encontrado is not None,
            'datos_ocr': resultado_ocr['datos_tecnicos']
        }
        
        if vehiculo_encontrado:
            response_data['vehiculo'] = AccesoVehiculoSerializer(
                vehiculo_encontrado, context={'request': request}
            ).data
            response_data['acceso_autorizado'] = vehiculo_encontrado.estado_acceso == 'autorizado'
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Error en el procesamiento OCR',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def procesar_ocr_placa(imagen, confianza_minima, pais_formato):
    """
    Simula el procesamiento OCR de placas
    En producción integrarías con servicios como AWS Textract, 
    Google Vision API, o bibliotecas como EasyOCR
    """
    import random
    import string
    
    # Simular detección de placa
    confianza = random.uniform(65.0, 98.0)
    placa_detectada = confianza >= float(confianza_minima)
    
    # Generar placa simulada según formato del país
    if pais_formato == 'BO':  # Bolivia
        placa_texto = f"{random.randint(1000, 9999)}-{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
    else:
        placa_texto = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    
    datos_tecnicos = {
        'bbox_placa': [random.randint(50, 100), random.randint(50, 100), 
                      random.randint(200, 400), random.randint(100, 200)],
        'caracteres_detectados': [
            {'caracter': c, 'confianza': random.uniform(80, 99)} 
            for c in placa_texto.replace('-', '')
        ],
        'formato_detectado': pais_formato,
        'calidad_imagen': random.choice(['excelente', 'buena', 'regular']),
        'processed_at': timezone.now().isoformat()
    }
    
    return {
        'placa_detectada': placa_detectada,
        'placa_texto': placa_texto if placa_detectada else '',
        'confianza': round(confianza, 2),
        'datos_tecnicos': datos_tecnicos
    }

# =====================================================================
# REGISTRO DE ACCESOS
# =====================================================================

class RegistroAccesoListCreateView(generics.ListCreateAPIView):
    """
    Lista y registra accesos al condominio
    """
    queryset = RegistroAcceso.objects.select_related(
        'usuario', 'visitante', 'vehiculo'
    )
    serializer_class = RegistroAccesoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['tipo_acceso', 'metodo_acceso', 'acceso_autorizado']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'visitante__nombres']
    ordering_fields = ['fecha_hora']
    ordering = ['-fecha_hora']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros por fecha
        fecha_desde = self.request.query_params.get('fecha_desde')
        fecha_hasta = self.request.query_params.get('fecha_hasta')
        
        if fecha_desde:
            queryset = queryset.filter(fecha_hora__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_hora__lte=fecha_hasta)
        
        # Filtro por ubicación
        ubicacion = self.request.query_params.get('ubicacion')
        if ubicacion:
            queryset = queryset.filter(ubicacion_acceso__icontains=ubicacion)
        
        return queryset

class RegistroAccesoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualiza registros de acceso
    """
    queryset = RegistroAcceso.objects.select_related(
        'usuario', 'visitante', 'vehiculo'
    )
    serializer_class = RegistroAccesoSerializer
    permission_classes = [IsAuthenticated, IsAdministradorOrSeguridad]

# =====================================================================
# INCIDENTES DE SEGURIDAD
# =====================================================================

class IncidenteSeguridadListCreateView(generics.ListCreateAPIView):
    """
    Lista y crea incidentes de seguridad con detección de anomalías
    """
    serializer_class = IncidenteSeguridadSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['tipo_incidente', 'nivel_gravedad', 'estado', 'detectado_por_ia']
    search_fields = ['titulo', 'descripcion', 'ubicacion']
    ordering_fields = ['fecha_incidente', 'nivel_gravedad']
    ordering = ['-fecha_incidente']
    
    def get_queryset(self):
        queryset = IncidenteSeguridad.objects.select_related(
            'usuario_involucrado', 'visitante_involucrado', 'vehiculo_involucrado',
            'reportado_por', 'asignado_a'
        )
        
        # Filtros adicionales
        solo_abiertos = self.request.query_params.get('solo_abiertos')
        if solo_abiertos == 'true':
            queryset = queryset.filter(estado__in=['abierto', 'en_investigacion'])
        
        nivel_minimo = self.request.query_params.get('nivel_minimo')
        if nivel_minimo:
            niveles_orden = {'bajo': 1, 'medio': 2, 'alto': 3, 'critico': 4}
            if nivel_minimo in niveles_orden:
                niveles_filtro = [k for k, v in niveles_orden.items() 
                                if v >= niveles_orden[nivel_minimo]]
                queryset = queryset.filter(nivel_gravedad__in=niveles_filtro)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IncidenteSeguridadListSerializer
        return IncidenteSeguridadSerializer
    
    def perform_create(self, serializer):
        serializer.save(reportado_por=self.request.user)

class IncidenteSeguridadDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualiza y elimina incidentes de seguridad
    """
    queryset = IncidenteSeguridad.objects.select_related(
        'usuario_involucrado', 'visitante_involucrado', 'vehiculo_involucrado',
        'reportado_por', 'asignado_a'
    )
    serializer_class = IncidenteSeguridadSerializer
    permission_classes = [IsAuthenticated]

# =====================================================================
# DETECCIÓN DE ANOMALÍAS POR IA
# =====================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detectar_anomalias(request):
    """
    Endpoint para detección de anomalías usando IA
    """
    serializer = DeteccionAnomaliaSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    archivo = serializer.validated_data['imagen_o_video']
    tipo_analisis = serializer.validated_data['tipo_analisis']
    zona_analisis = serializer.validated_data.get('zona_analisis')
    sensibilidad = serializer.validated_data['sensibilidad']
    
    try:
        # Procesar detección de anomalías
        resultado_ia = procesar_deteccion_anomalias(
            archivo, tipo_analisis, zona_analisis, sensibilidad
        )
        
        # Si se detecta anomalía, crear incidente automáticamente
        if resultado_ia['anomalia_detectada'] and resultado_ia['confianza'] >= 85.0:
            incidente = IncidenteSeguridad.objects.create(
                tipo_incidente='movimiento_anomalo',
                nivel_gravedad=determinar_nivel_gravedad(resultado_ia['confianza']),
                titulo=f"Anomalía detectada automáticamente - {tipo_analisis}",
                descripcion=f"El sistema de IA ha detectado una anomalía tipo '{tipo_analisis}' "
                           f"con {resultado_ia['confianza']}% de confianza.",
                ubicacion=resultado_ia.get('ubicacion_estimada', 'No especificada'),
                detectado_por_ia=True,
                algoritmo_deteccion=f"anomaly_detection_{tipo_analisis}",
                confianza_deteccion=resultado_ia['confianza'],
                estado='abierto',
                reportado_por=request.user,
                fecha_incidente=timezone.now(),
                datos_analisis_ia=resultado_ia
            )
            
            resultado_ia['incidente_creado'] = {
                'id': incidente.id,
                'codigo': incidente.codigo_incidente
            }
        
        return Response({
            'success': True,
            'anomalia_detectada': resultado_ia['anomalia_detectada'],
            'confianza': resultado_ia['confianza'],
            'tipo_anomalia': resultado_ia.get('tipo_anomalia'),
            'descripcion': resultado_ia.get('descripcion'),
            'datos_tecnicos': resultado_ia.get('datos_tecnicos'),
            'incidente_creado': resultado_ia.get('incidente_creado')
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Error en la detección de anomalías',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def procesar_deteccion_anomalias(archivo, tipo_analisis, zona_analisis, sensibilidad):
    """
    Simula el procesamiento de detección de anomalías
    En producción integrarías con modelos de ML para detección de anomalías
    """
    import random
    
    confianza = random.uniform(50.0, 95.0) * (float(sensibilidad) / 100)
    anomalia_detectada = confianza >= 70.0
    
    tipos_anomalia = {
        'movimiento': ['movimiento_rapido', 'movimiento_erratico', 'objeto_abandonado'],
        'presencia': ['persona_no_autorizada', 'presencia_nocturna', 'multitud'],
        'comportamiento': ['comportamiento_agresivo', 'actividad_sospechosa', 'loitering'],
        'objeto': ['objeto_peligroso', 'vehiculo_no_autorizado', 'item_perdido']
    }
    
    tipo_anomalia = random.choice(tipos_anomalia.get(tipo_analisis, ['anomalia_general']))
    
    datos_tecnicos = {
        'frames_analizados': random.randint(30, 300),
        'objetos_detectados': random.randint(1, 10),
        'zona_analisis_coords': zona_analisis or [0, 0, 100, 100],
        'timestamp_deteccion': timezone.now().isoformat(),
        'modelo_utilizado': f"anomaly_detector_v2.1_{tipo_analisis}",
        'sensibilidad_aplicada': float(sensibilidad)
    }
    
    return {
        'anomalia_detectada': anomalia_detectada,
        'confianza': round(confianza, 2),
        'tipo_anomalia': tipo_anomalia,
        'descripcion': f"Anomalía tipo {tipo_anomalia} detectada con {confianza:.1f}% de confianza",
        'ubicacion_estimada': f"Zona {random.choice(['A', 'B', 'C'])} - Cámara {random.randint(1, 8)}",
        'datos_tecnicos': datos_tecnicos
    }

def determinar_nivel_gravedad(confianza):
    """Determina el nivel de gravedad basado en la confianza de detección"""
    if confianza >= 95:
        return 'critico'
    elif confianza >= 85:
        return 'alto'
    elif confianza >= 70:
        return 'medio'
    else:
        return 'bajo'

# =====================================================================
# CONFIGURACIÓN DE IA
# =====================================================================

class ConfiguracionIAListCreateView(generics.ListCreateAPIView):
    """
    Lista y crea configuraciones de IA
    """
    queryset = ConfiguracionIA.objects.filter(esta_activo=True)
    serializer_class = ConfiguracionIASerializer
    permission_classes = [IsAuthenticated, IsAdministradorOrSeguridad]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'tipo_algoritmo']
    ordering_fields = ['nombre', 'fecha_creacion']
    ordering = ['nombre']
    
    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

class ConfiguracionIADetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualiza y elimina configuraciones de IA
    """
    queryset = ConfiguracionIA.objects.all()
    serializer_class = ConfiguracionIASerializer
    permission_classes = [IsAuthenticated, IsAdministradorOrSeguridad]
    
    def perform_destroy(self, instance):
        instance.esta_activo = False
        instance.save()

# =====================================================================
# ANÁLISIS PREDICTIVO DE MOROSIDAD
# =====================================================================

class AnalisisPredictivoMorosidadListView(generics.ListAPIView):
    """
    Lista análisis predictivos de morosidad
    """
    serializer_class = AnalisisPredictivoMorosidadSerializer
    permission_classes = [IsAuthenticated, IsAdministradorOrSeguridad]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    # filterset_fields = ['nivel_riesgo', 'unidad']
    ordering_fields = ['fecha_analisis', 'probabilidad_morosidad']
    ordering = ['-fecha_analisis']
    
    def get_queryset(self):
        return AnalisisPredictivoMorosidad.objects.select_related(
            'unidad', 'usuario_analizado', 'generado_por'
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdministradorOrSeguridad])
def generar_analisis_morosidad(request):
    """
    Genera análisis predictivo de morosidad usando IA
    """
    serializer = AnalisisMorosidadSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    unidad_id = serializer.validated_data['unidad_id']
    incluir_factores_externos = serializer.validated_data['incluir_factores_externos']
    
    try:
        unidad = UnidadHabitacional.objects.get(id=unidad_id)
        usuario = unidad.usuario_responsable
        
        # Obtener historial de pagos
        pagos_historial = Pago.objects.filter(
            unidad=unidad
        ).order_by('-fecha_creacion')[:12]  # Últimos 12 pagos
        
        # Procesar análisis de IA
        resultado_analisis = procesar_analisis_morosidad(
            unidad, usuario, pagos_historial, incluir_factores_externos
        )
        
        # Guardar análisis en base de datos
        analisis = AnalisisPredictivoMorosidad.objects.create(
            unidad=unidad,
            usuario_analizado=usuario,
            probabilidad_morosidad=resultado_analisis['probabilidad_morosidad'],
            nivel_riesgo=resultado_analisis['nivel_riesgo'],
            factores_riesgo=resultado_analisis['factores_riesgo'],
            historial_pagos_analizado=resultado_analisis['historial_resumen'],
            recomendaciones=resultado_analisis['recomendaciones'],
            acciones_sugeridas=resultado_analisis['acciones_sugeridas'],
            modelo_utilizado=resultado_analisis['modelo_utilizado'],
            version_modelo=resultado_analisis['version_modelo'],
            confianza_prediccion=resultado_analisis['confianza_prediccion'],
            valido_hasta=timezone.now() + timedelta(days=30),
            generado_por=request.user
        )
        
        # Serializar y retornar
        response_data = AnalisisPredictivoMorosidadSerializer(
            analisis, context={'request': request}
        ).data
        
        return Response({
            'success': True,
            'analisis': response_data,
            'mensaje': 'Análisis predictivo generado exitosamente'
        }, status=status.HTTP_201_CREATED)
        
    except UnidadHabitacional.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Unidad no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Error generando análisis predictivo',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def procesar_analisis_morosidad(unidad, usuario, pagos_historial, incluir_factores_externos):
    """
    Simula el procesamiento de análisis predictivo de morosidad
    En producción usarías modelos de ML como Random Forest, XGBoost, etc.
    """
    import random
    from collections import Counter
    
    # Análisis del historial de pagos
    pagos_data = []
    pagos_a_tiempo = 0
    pagos_tardios = 0
    monto_total_pagado = 0
    
    for pago in pagos_historial:
        pagos_data.append({
            'monto': float(pago.monto_total),
            'estado': pago.estado,
            'dias_retraso': (pago.fecha_pago - pago.fecha_vencimiento).days if pago.fecha_pago and pago.fecha_vencimiento else 0
        })
        
        if pago.estado == 'pagado':
            monto_total_pagado += float(pago.monto_total)
            if pago.fecha_pago and pago.fecha_vencimiento and pago.fecha_pago <= pago.fecha_vencimiento:
                pagos_a_tiempo += 1
            else:
                pagos_tardios += 1
    
    # Calcular métricas base
    total_pagos = len(pagos_data)
    tasa_pago_a_tiempo = (pagos_a_tiempo / total_pagos * 100) if total_pagos > 0 else 0
    
    # Factores de riesgo
    factores_riesgo = {}
    factores_riesgo['historial_pagos'] = {
        'total_pagos': total_pagos,
        'pagos_a_tiempo': pagos_a_tiempo,
        'pagos_tardios': pagos_tardios,
        'tasa_pago_a_tiempo': round(tasa_pago_a_tiempo, 2),
        'monto_total_pagado': monto_total_pagado
    }
    
    # Factores adicionales (simulados)
    if incluir_factores_externos:
        factores_riesgo['factores_externos'] = {
            'antiguedad_residencia': random.randint(1, 10),
            'nivel_ingresos_estimado': random.choice(['bajo', 'medio', 'alto']),
            'historial_incidentes': random.randint(0, 3),
            'participacion_actividades': random.choice(['baja', 'media', 'alta'])
        }
    
    # Calcular probabilidad (algoritmo simplificado)
    probabilidad_base = max(0, 100 - tasa_pago_a_tiempo)
    
    # Ajustes por factores externos
    if incluir_factores_externos:
        if factores_riesgo['factores_externos']['nivel_ingresos_estimado'] == 'bajo':
            probabilidad_base += 15
        elif factores_riesgo['factores_externos']['nivel_ingresos_estimado'] == 'alto':
            probabilidad_base -= 10
        
        probabilidad_base += factores_riesgo['factores_externos']['historial_incidentes'] * 5
    
    probabilidad_morosidad = min(95, max(5, probabilidad_base + random.uniform(-10, 10)))
    
    # Determinar nivel de riesgo
    if probabilidad_morosidad >= 80:
        nivel_riesgo = 'muy_alto'
    elif probabilidad_morosidad >= 60:
        nivel_riesgo = 'alto'
    elif probabilidad_morosidad >= 40:
        nivel_riesgo = 'medio'
    elif probabilidad_morosidad >= 20:
        nivel_riesgo = 'bajo'
    else:
        nivel_riesgo = 'muy_bajo'
    
    # Generar recomendaciones
    recomendaciones = generar_recomendaciones_morosidad(probabilidad_morosidad, factores_riesgo)
    
    return {
        'probabilidad_morosidad': round(probabilidad_morosidad, 2),
        'nivel_riesgo': nivel_riesgo,
        'factores_riesgo': factores_riesgo,
        'historial_resumen': {
            'pagos_analizados': total_pagos,
            'tasa_cumplimiento': round(tasa_pago_a_tiempo, 2),
            'monto_total': monto_total_pagado
        },
        'recomendaciones': recomendaciones['texto'],
        'acciones_sugeridas': recomendaciones['acciones'],
        'modelo_utilizado': 'morosidad_predictor_v1.2',
        'version_modelo': '1.2.0',
        'confianza_prediccion': round(random.uniform(75, 95), 2)
    }

def generar_recomendaciones_morosidad(probabilidad, factores):
    """Genera recomendaciones basadas en el análisis predictivo"""
    
    recomendaciones_texto = []
    acciones_sugeridas = []
    
    if probabilidad >= 80:
        recomendaciones_texto.append(
            "RIESGO MUY ALTO: Se recomienda contacto inmediato con el residente "
            "para establecer un plan de pagos personalizado."
        )
        acciones_sugeridas.extend([
            "Contactar al residente en 24 horas",
            "Ofrecer plan de pagos flexible",
            "Evaluar situación financiera personal",
            "Considerar mediación administrativa"
        ])
    elif probabilidad >= 60:
        recomendaciones_texto.append(
            "RIESGO ALTO: Monitoreo cercano y comunicación proactiva recomendada."
        )
        acciones_sugeridas.extend([
            "Enviar recordatorio de pago anticipado",
            "Ofrecer facilidades de pago",
            "Programar seguimiento semanal"
        ])
    elif probabilidad >= 40:
        recomendaciones_texto.append(
            "RIESGO MEDIO: Mantener comunicación regular y monitoreo."
        )
        acciones_sugeridas.extend([
            "Enviar recordatorios automáticos",
            "Monitorear puntualidad de pagos",
            "Ofrecer canales de pago adicionales"
        ])
    else:
        recomendaciones_texto.append(
            "RIESGO BAJO: Continuar con procedimientos normales de cobranza."
        )
        acciones_sugeridas.extend([
            "Mantener comunicación estándar",
            "Reconocer buen historial de pagos"
        ])
    
    # Agregar recomendaciones específicas basadas en factores
    if factores.get('historial_pagos', {}).get('tasa_pago_a_tiempo', 0) < 50:
        recomendaciones_texto.append(
            "Historial de pagos tardíos detectado. Considerar incentivos por pago puntual."
        )
    
    return {
        'texto': ' '.join(recomendaciones_texto),
        'acciones': acciones_sugeridas
    }

# =====================================================================
# DASHBOARDS Y REPORTES
# =====================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_seguridad(request):
    """
    Dashboard con métricas de seguridad en tiempo real
    """
    try:
        # Fechas para filtros
        hoy = timezone.now().date()
        hace_7_dias = hoy - timedelta(days=7)
        hace_30_dias = hoy - timedelta(days=30)
        
        # Métricas de visitantes
        visitantes_hoy = RegistroVisitante.objects.filter(
            fecha_creacion__date=hoy
        ).count()
        
        visitantes_en_complejo = RegistroVisitante.objects.filter(
            estado='en_visita'
        ).count()
        
        # Métricas de accesos
        accesos_hoy = RegistroAcceso.objects.filter(
            fecha_hora__date=hoy
        ).count()
        
        accesos_no_autorizados = RegistroAcceso.objects.filter(
            acceso_autorizado=False,
            fecha_hora__gte=hace_7_dias
        ).count()
        
        # Métricas de incidentes
        incidentes_abiertos = IncidenteSeguridad.objects.filter(
            estado__in=['abierto', 'en_investigacion']
        ).count()
        
        incidentes_criticos = IncidenteSeguridad.objects.filter(
            nivel_gravedad='critico',
            estado__in=['abierto', 'en_investigacion']
        ).count()
        
        incidentes_ia = IncidenteSeguridad.objects.filter(
            detectado_por_ia=True,
            fecha_incidente__gte=hace_30_dias
        ).count()
        
        # Métricas de vehículos
        vehiculos_registrados = AccesoVehiculo.objects.filter(
            esta_activo=True
        ).count()
        
        # Análisis predictivo
        analisis_riesgo_alto = AnalisisPredictivoMorosidad.objects.filter(
            nivel_riesgo__in=['alto', 'muy_alto'],
            valido_hasta__gte=timezone.now()
        ).count()
        
        # Estadísticas de IA
        configuraciones_ia_activas = ConfiguracionIA.objects.filter(
            esta_activo=True
        ).count()
        
        dashboard_data = {
            'visitantes': {
                'hoy': visitantes_hoy,
                'en_complejo': visitantes_en_complejo,
                'total_registrados': RegistroVisitante.objects.count()
            },
            'accesos': {
                'hoy': accesos_hoy,
                'no_autorizados_7d': accesos_no_autorizados,
                'total_registros': RegistroAcceso.objects.count()
            },
            'incidentes': {
                'abiertos': incidentes_abiertos,
                'criticos': incidentes_criticos,
                'detectados_ia_30d': incidentes_ia,
                'total': IncidenteSeguridad.objects.count()
            },
            'vehiculos': {
                'registrados': vehiculos_registrados,
                'autorizados': AccesoVehiculo.objects.filter(
                    estado_acceso='autorizado', esta_activo=True
                ).count()
            },
            'predicciones': {
                'riesgo_alto_morosidad': analisis_riesgo_alto,
                'configuraciones_ia': configuraciones_ia_activas
            },
            'fecha_actualizacion': timezone.now().isoformat()
        }
        
        return Response({
            'success': True,
            'dashboard': dashboard_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Error generando dashboard',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdministradorOrSeguridad])
def reporte_seguridad_periodo(request):
    """
    Genera reporte de seguridad para un período específico
    """
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')
    
    if not fecha_inicio or not fecha_fin:
        return Response({
            'success': False,
            'error': 'Se requieren fecha_inicio y fecha_fin'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Convertir fechas
        inicio = datetime.fromisoformat(fecha_inicio.replace('Z', '+00:00'))
        fin = datetime.fromisoformat(fecha_fin.replace('Z', '+00:00'))
        
        # Generar reporte
        reporte = {
            'periodo': {
                'inicio': fecha_inicio,
                'fin': fecha_fin,
                'dias': (fin - inicio).days + 1
            },
            'visitantes': {
                'total_registrados': RegistroVisitante.objects.filter(
                    fecha_creacion__range=[inicio, fin]
                ).count(),
                'por_estado': dict(RegistroVisitante.objects.filter(
                    fecha_creacion__range=[inicio, fin]
                ).values_list('estado').annotate(Count('estado')))
            },
            'accesos': {
                'total': RegistroAcceso.objects.filter(
                    fecha_hora__range=[inicio, fin]
                ).count(),
                'autorizados': RegistroAcceso.objects.filter(
                    fecha_hora__range=[inicio, fin],
                    acceso_autorizado=True
                ).count(),
                'no_autorizados': RegistroAcceso.objects.filter(
                    fecha_hora__range=[inicio, fin],
                    acceso_autorizado=False
                ).count()
            },
            'incidentes': {
                'total': IncidenteSeguridad.objects.filter(
                    fecha_incidente__range=[inicio, fin]
                ).count(),
                'por_gravedad': dict(IncidenteSeguridad.objects.filter(
                    fecha_incidente__range=[inicio, fin]
                ).values_list('nivel_gravedad').annotate(Count('nivel_gravedad'))),
                'detectados_ia': IncidenteSeguridad.objects.filter(
                    fecha_incidente__range=[inicio, fin],
                    detectado_por_ia=True
                ).count()
            }
        }
        
        return Response({
            'success': True,
            'reporte': reporte
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Error generando reporte',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
