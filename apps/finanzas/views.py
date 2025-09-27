from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import UnidadHabitacional, TipoPago, Pago, HistorialPago, Multa
from .serializers import (
    SerializadorUnidadHabitacional, SerializadorTipoPago, SerializadorPago,
    SerializadorCrearPago, SerializadorProcesarPago, SerializadorMulta,
    SerializadorResumenFinanciero
)

class ListaUnidadesHabitacionales(generics.ListCreateAPIView):
    """
    Listar y crear unidades habitacionales
    """
    queryset = UnidadHabitacional.objects.filter(esta_activa=True)
    serializer_class = SerializadorUnidadHabitacional
    permission_classes = [permissions.IsAuthenticated]

class DetalleUnidadHabitacional(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar unidad habitacional
    """
    queryset = UnidadHabitacional.objects.all()
    serializer_class = SerializadorUnidadHabitacional
    permission_classes = [permissions.IsAuthenticated]

class ListaTiposPago(generics.ListCreateAPIView):
    """
    Listar y crear tipos de pago
    """
    queryset = TipoPago.objects.filter(esta_activo=True)
    serializer_class = SerializadorTipoPago
    permission_classes = [permissions.IsAuthenticated]

class ListaPagosUsuario(generics.ListAPIView):
    """
    Listar pagos del usuario autenticado
    """
    serializer_class = SerializadorPago
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        usuario = self.request.user
        # Obtener pagos donde el usuario es responsable (propietario o inquilino)
        unidades_responsable = UnidadHabitacional.objects.filter(
            Q(propietario=usuario) | Q(inquilino=usuario)
        )
        return Pago.objects.filter(unidad__in=unidades_responsable)

class ListaPagosAdmin(generics.ListCreateAPIView):
    """
    Listar todos los pagos (solo administradores)
    """
    queryset = Pago.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SerializadorCrearPago
        return SerializadorPago
    
    def get_queryset(self):
        queryset = Pago.objects.all()
        
        # Filtros opcionales
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
            
        unidad = self.request.query_params.get('unidad', None)
        if unidad:
            queryset = queryset.filter(unidad_id=unidad)
            
        periodo = self.request.query_params.get('periodo', None)
        if periodo:
            queryset = queryset.filter(periodo=periodo)
            
        vencidos = self.request.query_params.get('vencidos', None)
        if vencidos == 'true':
            queryset = queryset.filter(
                fecha_vencimiento__lt=timezone.now().date(),
                estado='pendiente'
            )
        
        return queryset.order_by('-fecha_vencimiento')

class DetallePago(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar pago específico
    """
    queryset = Pago.objects.all()
    serializer_class = SerializadorPago
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def procesar_pago(request, pago_id):
    """
    Procesar un pago específico
    """
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return Response({
            'error': 'Pago no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializador = SerializadorProcesarPago(
        data=request.data, 
        context={'pago': pago, 'request': request}
    )
    
    if serializador.is_valid():
        monto_pago = serializador.validated_data['monto_pago']
        metodo_pago = serializador.validated_data['metodo_pago']
        referencia = serializador.validated_data.get('referencia', '')
        observaciones = serializador.validated_data.get('observaciones', '')
        comprobante = serializador.validated_data.get('comprobante')
        
        # Guardar estado anterior
        estado_anterior = pago.estado
        
        # Actualizar montos
        pago.monto_pagado += monto_pago
        
        # Determinar nuevo estado
        if pago.monto_pagado >= pago.monto_total:
            pago.estado = 'pagado'
            pago.fecha_pago = timezone.now()
        elif pago.monto_pagado > Decimal('0.00'):
            pago.estado = 'parcial'
        
        # Actualizar comprobante si se proporciona
        if comprobante:
            pago.comprobante = comprobante
        
        # Actualizar referencia de pago
        if referencia:
            pago.referencia_pago = referencia
        
        pago.save()
        
        # Crear registro en historial
        HistorialPago.objects.create(
            pago=pago,
            monto_transaccion=monto_pago,
            estado_anterior=estado_anterior,
            estado_nuevo=pago.estado,
            metodo_pago=metodo_pago,
            referencia=referencia,
            observaciones=observaciones,
            procesado_por=request.user
        )
        
        return Response({
            'mensaje': 'Pago procesado exitosamente',
            'pago': SerializadorPago(pago).data
        })
    
    return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def historial_pagos_usuario(request):
    """
    Obtener historial de pagos del usuario
    """
    usuario = request.user
    unidades = UnidadHabitacional.objects.filter(
        Q(propietario=usuario) | Q(inquilino=usuario)
    )
    
    # Filtrar por fechas si se proporcionan
    fecha_desde = request.query_params.get('fecha_desde')
    fecha_hasta = request.query_params.get('fecha_hasta')
    
    pagos = Pago.objects.filter(unidad__in=unidades)
    
    if fecha_desde:
        pagos = pagos.filter(fecha_creacion__gte=fecha_desde)
    if fecha_hasta:
        pagos = pagos.filter(fecha_creacion__lte=fecha_hasta)
    
    pagos = pagos.order_by('-fecha_creacion')
    serializador = SerializadorPago(pagos, many=True)
    
    return Response({
        'historial': serializador.data,
        'total_pagos': pagos.count()
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def resumen_financiero_usuario(request):
    """
    Resumen financiero para el usuario autenticado
    """
    usuario = request.user
    unidades = UnidadHabitacional.objects.filter(
        Q(propietario=usuario) | Q(inquilino=usuario)
    )
    
    # Calcular totales
    pagos_pendientes = Pago.objects.filter(
        unidad__in=unidades, 
        estado__in=['pendiente', 'parcial']
    )
    
    total_pendiente = pagos_pendientes.aggregate(
        total=Sum('monto_total') - Sum('monto_pagado')
    )['total'] or Decimal('0.00')
    
    pagos_vencidos = pagos_pendientes.filter(
        fecha_vencimiento__lt=timezone.now().date()
    ).count()
    
    # Pagos del mes actual
    mes_actual = timezone.now().replace(day=1)
    pagos_mes = Pago.objects.filter(
        unidad__in=unidades,
        fecha_pago__gte=mes_actual
    )
    total_pagado_mes = pagos_mes.aggregate(
        total=Sum('monto_pagado')
    )['total'] or Decimal('0.00')
    
    # Multas pendientes
    multas_pendientes = Multa.objects.filter(
        unidad__in=unidades,
        esta_pagada=False
    )
    total_multas = multas_pendientes.aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')
    
    return Response({
        'total_pendiente': total_pendiente,
        'total_pagado_mes': total_pagado_mes,
        'pagos_vencidos': pagos_vencidos,
        'total_multas_pendientes': total_multas,
        'proximos_vencimientos': SerializadorPago(
            pagos_pendientes.filter(
                fecha_vencimiento__lte=timezone.now().date() + timedelta(days=7)
            )[:5], many=True
        ).data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def resumen_financiero_admin(request):
    """
    Resumen financiero completo para administradores
    """
    # Totales generales
    total_pendiente = Pago.objects.filter(
        estado__in=['pendiente', 'parcial']
    ).aggregate(
        total=Sum('monto_total') - Sum('monto_pagado')
    )['total'] or Decimal('0.00')
    
    # Pagos del mes
    mes_actual = timezone.now().replace(day=1)
    total_pagado_mes = Pago.objects.filter(
        fecha_pago__gte=mes_actual
    ).aggregate(
        total=Sum('monto_pagado')
    )['total'] or Decimal('0.00')
    
    # Pagos vencidos
    pagos_vencidos = Pago.objects.filter(
        fecha_vencimiento__lt=timezone.now().date(),
        estado='pendiente'
    ).count()
    
    # Multas pendientes
    total_multas_pendientes = Multa.objects.filter(
        esta_pagada=False
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')
    
    # Unidades morosas (con pagos vencidos)
    unidades_morosas = UnidadHabitacional.objects.filter(
        pagos__fecha_vencimiento__lt=timezone.now().date(),
        pagos__estado='pendiente'
    ).distinct().count()
    
    # Tasa de cobranza del mes
    total_esperado_mes = Pago.objects.filter(
        fecha_vencimiento__year=timezone.now().year,
        fecha_vencimiento__month=timezone.now().month
    ).aggregate(
        total=Sum('monto_total')
    )['total'] or Decimal('0.00')
    
    tasa_cobranza = Decimal('0.00')
    if total_esperado_mes > 0:
        tasa_cobranza = (total_pagado_mes / total_esperado_mes * 100).quantize(Decimal('0.01'))
    
    return Response({
        'total_pendiente': total_pendiente,
        'total_pagado_mes': total_pagado_mes,
        'pagos_vencidos': pagos_vencidos,
        'total_multas_pendientes': total_multas_pendientes,
        'unidades_morosas': unidades_morosas,
        'tasa_cobranza': tasa_cobranza,
        'estadisticas_por_estado': Pago.objects.values('estado').annotate(
            cantidad=Count('id'),
            monto_total=Sum('monto_total')
        )
    })

class ListaMultas(generics.ListCreateAPIView):
    """
    Listar y crear multas
    """
    queryset = Multa.objects.all()
    serializer_class = SerializadorMulta
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Multa.objects.all()
        
        # Si no es admin, solo ver multas de sus unidades
        if not self.request.user.is_staff:
            unidades = UnidadHabitacional.objects.filter(
                Q(propietario=self.request.user) | Q(inquilino=self.request.user)
            )
            queryset = queryset.filter(unidad__in=unidades)
        
        # Filtros opcionales
        unidad = self.request.query_params.get('unidad')
        if unidad:
            queryset = queryset.filter(unidad_id=unidad)
            
        pendientes = self.request.query_params.get('pendientes')
        if pendientes == 'true':
            queryset = queryset.filter(esta_pagada=False)
        
        return queryset.order_by('-fecha_creacion')
    
    def perform_create(self, serializer):
        serializer.save(aplicada_por=self.request.user)

class DetalleMulta(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar multa específica
    """
    queryset = Multa.objects.all()
    serializer_class = SerializadorMulta
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generar_pagos_mensuales(request):
    """
    Generar pagos mensuales automáticamente
    """
    periodo = request.data.get('periodo')  # Formato: YYYY-MM
    tipos_pago = request.data.get('tipos_pago', [])  # IDs de tipos de pago
    
    if not periodo:
        return Response({
            'error': 'Debe especificar el período'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validar formato del período
    try:
        fecha_periodo = datetime.strptime(periodo, '%Y-%m')
    except ValueError:
        return Response({
            'error': 'Formato de período inválido. Use YYYY-MM'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Obtener tipos de pago a generar
    if tipos_pago:
        tipos = TipoPago.objects.filter(id__in=tipos_pago, esta_activo=True)
    else:
        tipos = TipoPago.objects.filter(es_recurrente=True, esta_activo=True)
    
    # Obtener todas las unidades activas
    unidades = UnidadHabitacional.objects.filter(esta_activa=True)
    
    pagos_creados = []
    errores = []
    
    for unidad in unidades:
        for tipo_pago in tipos:
            # Verificar si ya existe pago para este período
            existe_pago = Pago.objects.filter(
                unidad=unidad,
                tipo_pago=tipo_pago,
                periodo=periodo
            ).exists()
            
            if not existe_pago:
                try:
                    # Calcular fecha de vencimiento (último día del mes)
                    from calendar import monthrange
                    año, mes = fecha_periodo.year, fecha_periodo.month
                    ultimo_dia = monthrange(año, mes)[1]
                    fecha_vencimiento = datetime(año, mes, ultimo_dia).date()
                    
                    pago = Pago.objects.create(
                        unidad=unidad,
                        usuario_pagador=unidad.usuario_responsable,
                        tipo_pago=tipo_pago,
                        monto_total=tipo_pago.monto_base,
                        fecha_vencimiento=fecha_vencimiento,
                        periodo=periodo,
                        descripcion=f"Pago {tipo_pago.nombre} - {periodo}",
                        creado_por=request.user
                    )
                    pagos_creados.append(pago.id)
                    
                except Exception as e:
                    errores.append(f"Error en unidad {unidad}: {str(e)}")
    
    return Response({
        'mensaje': f'Pagos generados para el período {periodo}',
        'pagos_creados': len(pagos_creados),
        'errores': errores,
        'detalles': {
            'periodo': periodo,
            'unidades_procesadas': unidades.count(),
            'tipos_pago_procesados': tipos.count()
        }
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def reporte_morosidad(request):
    """
    Generar reporte de morosidad
    """
    # Obtener parámetros de filtro
    dias_vencido = int(request.query_params.get('dias_vencido', 30))
    
    # Pagos vencidos
    fecha_limite = timezone.now().date() - timedelta(days=dias_vencido)
    
    pagos_vencidos = Pago.objects.filter(
        fecha_vencimiento__lt=timezone.now().date(),
        estado='pendiente'
    ).select_related('unidad', 'tipo_pago', 'usuario_pagador')
    
    # Agrupar por unidad
    unidades_morosas = {}
    total_deuda = Decimal('0.00')
    
    for pago in pagos_vencidos:
        unidad_key = pago.unidad.id
        if unidad_key not in unidades_morosas:
            unidades_morosas[unidad_key] = {
                'unidad': SerializadorUnidadHabitacional(pago.unidad).data,
                'pagos_vencidos': [],
                'total_deuda': Decimal('0.00'),
                'dias_max_vencido': 0
            }
        
        unidades_morosas[unidad_key]['pagos_vencidos'].append(
            SerializadorPago(pago).data
        )
        unidades_morosas[unidad_key]['total_deuda'] += pago.saldo_pendiente
        unidades_morosas[unidad_key]['dias_max_vencido'] = max(
            unidades_morosas[unidad_key]['dias_max_vencido'],
            pago.dias_vencido
        )
        total_deuda += pago.saldo_pendiente
    
    return Response({
        'resumen': {
            'total_unidades_morosas': len(unidades_morosas),
            'total_deuda': total_deuda,
            'promedio_deuda_por_unidad': total_deuda / len(unidades_morosas) if unidades_morosas else Decimal('0.00'),
            'fecha_corte': timezone.now().date(),
            'criterio_dias': dias_vencido
        },
        'detalle_unidades': list(unidades_morosas.values())
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def aplicar_interes_moratorio(request):
    """
    Aplicar interés moratorio a pagos vencidos
    """
    tasa_interes = Decimal(request.data.get('tasa_interes', '0.05'))  # 5% por defecto
    dias_gracia = int(request.data.get('dias_gracia', 30))  # 30 días de gracia
    
    fecha_limite = timezone.now().date() - timedelta(days=dias_gracia)
    
    pagos_vencidos = Pago.objects.filter(
        fecha_vencimiento__lt=fecha_limite,
        estado='pendiente'
    )
    
    intereses_aplicados = []
    
    for pago in pagos_vencidos:
        # Calcular interés
        dias_vencimiento = (timezone.now().date() - pago.fecha_vencimiento).days - dias_gracia
        if dias_vencimiento > 0:
            interes = pago.saldo_pendiente * tasa_interes * (dias_vencimiento / 30)
            interes = interes.quantize(Decimal('0.01'))
            
            if interes > Decimal('0.00'):
                # Crear multa por interés moratorio
                multa = Multa.objects.create(
                    unidad=pago.unidad,
                    tipo_multa='retraso_pago',
                    monto=interes,
                    descripcion=f'Interés moratorio por {dias_vencimiento} días de retraso en pago {pago.id}',
                    fecha_infraccion=timezone.now().date(),
                    aplicada_por=request.user
                )
                
                intereses_aplicados.append({
                    'pago_id': pago.id,
                    'unidad': str(pago.unidad),
                    'interes_aplicado': interes,
                    'dias_vencimiento': dias_vencimiento,
                    'multa_id': multa.id
                })
    
    return Response({
        'mensaje': f'Intereses moratorios aplicados',
        'total_intereses': len(intereses_aplicados),
        'detalle': intereses_aplicados,
        'parametros': {
            'tasa_interes': f'{tasa_interes * 100}%',
            'dias_gracia': dias_gracia,
            'fecha_corte': fecha_limite
        }
    })