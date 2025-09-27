from rest_framework import serializers
from decimal import Decimal
from django.utils import timezone
from .models import UnidadHabitacional, TipoPago, Pago, HistorialPago, Multa
from apps.autenticacion.models import Usuario

class SerializadorUnidadHabitacional(serializers.ModelSerializer):
    """
    Serializador para las unidades habitacionales
    """
    nombre_propietario = serializers.CharField(source='propietario.get_full_name', read_only=True)
    nombre_inquilino = serializers.CharField(source='inquilino.get_full_name', read_only=True)
    usuario_responsable_nombre = serializers.CharField(source='usuario_responsable.get_full_name', read_only=True)
    
    class Meta:
        model = UnidadHabitacional
        fields = [
            'id', 'numero_unidad', 'edificio', 'propietario', 'inquilino',
            'area_m2', 'dormitorios', 'esta_activa', 'nombre_propietario',
            'nombre_inquilino', 'usuario_responsable_nombre'
        ]

class SerializadorTipoPago(serializers.ModelSerializer):
    """
    Serializador para los tipos de pago
    """
    class Meta:
        model = TipoPago
        fields = '__all__'

class SerializadorHistorialPago(serializers.ModelSerializer):
    """
    Serializador para el historial de pagos
    """
    procesado_por_nombre = serializers.CharField(source='procesado_por.get_full_name', read_only=True)
    
    class Meta:
        model = HistorialPago
        fields = [
            'id', 'monto_transaccion', 'estado_anterior', 'estado_nuevo',
            'metodo_pago', 'referencia', 'observaciones', 'procesado_por_nombre',
            'fecha_transaccion'
        ]

class SerializadorPago(serializers.ModelSerializer):
    """
    Serializador principal para los pagos
    """
    unidad_info = SerializadorUnidadHabitacional(source='unidad', read_only=True)
    tipo_pago_info = SerializadorTipoPago(source='tipo_pago', read_only=True)
    usuario_pagador_nombre = serializers.CharField(source='usuario_pagador.get_full_name', read_only=True)
    historial = SerializadorHistorialPago(many=True, read_only=True)
    saldo_pendiente = serializers.ReadOnlyField()
    esta_vencido = serializers.ReadOnlyField()
    dias_vencido = serializers.ReadOnlyField()
    
    class Meta:
        model = Pago
        fields = [
            'id', 'unidad', 'usuario_pagador', 'tipo_pago', 'monto_total',
            'monto_pagado', 'estado', 'fecha_vencimiento', 'fecha_pago',
            'periodo', 'descripcion', 'observaciones', 'referencia_pago',
            'comprobante', 'fecha_creacion', 'unidad_info', 'tipo_pago_info',
            'usuario_pagador_nombre', 'historial', 'saldo_pendiente',
            'esta_vencido', 'dias_vencido'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

class SerializadorCrearPago(serializers.ModelSerializer):
    """
    Serializador para crear nuevos pagos
    """
    class Meta:
        model = Pago
        fields = [
            'unidad', 'usuario_pagador', 'tipo_pago', 'monto_total',
            'fecha_vencimiento', 'periodo', 'descripcion', 'observaciones'
        ]
    
    def create(self, validated_data):
        """Crear pago y asignar usuario creador"""
        validated_data['creado_por'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_periodo(self, value):
        """Validar formato del período"""
        import re
        if not re.match(r'^\d{4}-\d{2}$', value):
            raise serializers.ValidationError("El período debe tener formato YYYY-MM")
        return value

class SerializadorProcesarPago(serializers.Serializer):
    """
    Serializador para procesar pagos
    """
    monto_pago = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=Decimal('0.01')
    )
    metodo_pago = serializers.ChoiceField(choices=[
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('deposito', 'Depósito Bancario'),
        ('cheque', 'Cheque'),
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('qr', 'Código QR'),
        ('otro', 'Otro'),
    ])
    referencia = serializers.CharField(max_length=100, required=False, allow_blank=True)
    observaciones = serializers.CharField(required=False, allow_blank=True)
    comprobante = serializers.ImageField(required=False)
    
    def validate_monto_pago(self, value):
        """Validar que el monto no exceda el saldo pendiente"""
        pago = self.context.get('pago')
        if pago and value > pago.saldo_pendiente:
            raise serializers.ValidationError(
                f"El monto no puede exceder el saldo pendiente (${pago.saldo_pendiente})"
            )
        return value

class SerializadorMulta(serializers.ModelSerializer):
    """
    Serializador para las multas
    """
    unidad_info = SerializadorUnidadHabitacional(source='unidad', read_only=True)
    aplicada_por_nombre = serializers.CharField(source='aplicada_por.get_full_name', read_only=True)
    tipo_multa_display = serializers.CharField(source='get_tipo_multa_display', read_only=True)
    
    class Meta:
        model = Multa
        fields = [
            'id', 'unidad', 'tipo_multa', 'monto', 'descripcion',
            'fecha_infraccion', 'esta_pagada', 'pago_asociado',
            'fecha_creacion', 'unidad_info', 'aplicada_por_nombre',
            'tipo_multa_display'
        ]
        read_only_fields = ['fecha_creacion']

class SerializadorResumenFinanciero(serializers.Serializer):
    """
    Serializador para el resumen financiero
    """
    total_pendiente = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_pagado_mes = serializers.DecimalField(max_digits=12, decimal_places=2)
    pagos_vencidos = serializers.IntegerField()
    total_multas_pendientes = serializers.DecimalField(max_digits=12, decimal_places=2)
    unidades_morosas = serializers.IntegerField()
    tasa_cobranza = serializers.DecimalField(max_digits=5, decimal_places=2)