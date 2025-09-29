from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import (
    TipoVisitante, RegistroVisitante, AccesoVehiculo, 
    RegistroAcceso, IncidenteSeguridad, ConfiguracionIA,
    AnalisisPredictivoMorosidad
)
from apps.autenticacion.models import PerfilUsuario

Usuario = get_user_model()

class SeguridadModelsTest(TestCase):
    """Tests para los modelos del módulo de seguridad"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.perfil = PerfilUsuario.objects.create(
            usuario=self.usuario,
            rol='propietario',
            numero_unidad='101',
            edificio='A'
        )
        
        self.tipo_visitante = TipoVisitante.objects.create(
            nombre='Familiar',
            descripcion='Familiares de residentes',
            requiere_autorizacion=True
        )
    
    def test_tipo_visitante_creation(self):
        """Test de creación de tipo de visitante"""
        self.assertEqual(str(self.tipo_visitante), 'Familiar')
        self.assertTrue(self.tipo_visitante.requiere_autorizacion)
        self.assertTrue(self.tipo_visitante.activo)
    
    def test_registro_visitante_creation(self):
        """Test de creación de registro de visitante"""
        registro = RegistroVisitante.objects.create(
            nombre_completo='Juan Pérez',
            documento_identidad='12345678',
            tipo_visitante=self.tipo_visitante,
            unidad_destino=self.perfil,
            motivo_visita='Visita familiar',
            telefono_contacto='70000000'
        )
        
        self.assertEqual(str(registro), 'Juan Pérez - 101')
        self.assertEqual(registro.estado, 'pendiente')
    
    def test_acceso_vehiculo_creation(self):
        """Test de creación de acceso de vehículo"""
        acceso = AccesoVehiculo.objects.create(
            placa_vehiculo='ABC123',
            propietario_vehiculo='Juan Pérez',
            tipo_vehiculo='auto',
            marca='Toyota',
            modelo='Corolla',
            color='Blanco',
            unidad_residente=self.perfil
        )
        
        self.assertEqual(str(acceso), 'ABC123 - Toyota Corolla')
        self.assertEqual(acceso.estado_acceso, 'activo')
    
    def test_configuracion_ia_creation(self):
        """Test de creación de configuración IA"""
        config = ConfiguracionIA.objects.create(
            servicio='reconocimiento_facial',
            configuracion_json={'precision': 0.95, 'modelo': 'v2.1'},
            activo=True
        )
        
        self.assertEqual(str(config), 'reconocimiento_facial')
        self.assertTrue(config.activo)

class SeguridadAPITest(APITestCase):
    """Tests para las APIs del módulo de seguridad"""
    
    def setUp(self):
        """Configuración inicial para tests de API"""
        self.usuario_admin = Usuario.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        
        self.perfil_admin = PerfilUsuario.objects.create(
            usuario=self.usuario_admin,
            rol='administrador',
            numero_unidad='Admin',
            edificio='Admin'
        )
        
        self.tipo_visitante = TipoVisitante.objects.create(
            nombre='Proveedor',
            descripcion='Proveedores de servicios',
            requiere_autorizacion=False
        )
    
    def test_dashboard_seguridad_unauthorized(self):
        """Test de acceso no autorizado al dashboard"""
        url = reverse('seguridad:dashboard-seguridad')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_tipos_visitante_list(self):
        """Test de listado de tipos de visitante"""
        self.client.force_authenticate(user=self.usuario_admin)
        url = reverse('seguridad:tipos-visitante-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class SeguridadUtilsTest(TestCase):
    """Tests para utilidades del módulo de seguridad"""
    
    def test_analisis_predictivo_creation(self):
        """Test de creación de análisis predictivo"""
        usuario = Usuario.objects.create_user(
            username='moroso_test',
            email='moroso@example.com',
            password='testpass123'
        )
        
        perfil = PerfilUsuario.objects.create(
            usuario=usuario,
            rol='propietario',
            numero_unidad='201',
            edificio='B'
        )
        
        analisis = AnalisisPredictivoMorosidad.objects.create(
            usuario=perfil,
            probabilidad_morosidad=Decimal('0.75'),
            nivel_riesgo='alto',
            factores_riesgo={'historial_pagos': 'irregular', 'monto_deuda': 'alto'},
            recomendaciones={'accion': 'contactar_inmediato', 'plan_pago': True}
        )
        
        self.assertEqual(str(analisis), 'Análisis - 201 - alto')
        self.assertEqual(analisis.nivel_riesgo, 'alto')
        self.assertEqual(analisis.probabilidad_morosidad, Decimal('0.75'))
