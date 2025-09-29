#!/usr/bin/env python3
"""
Script para limpiar todos los datos de la base de datos del condominio
manteniendo solo las migraciones y la estructura de las tablas.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_condominium.settings.development')
django.setup()

from django.contrib.auth.models import Group
from apps.autenticacion.models import Usuario, PerfilUsuario
from apps.finanzas.models import *
from apps.comunicacion.models import *
from apps.reservas.models import *
from apps.seguridad.models import *
from apps.mantenimiento.models import *

def clear_all_data():
    """Limpiar todos los datos de la base de datos"""
    print("🧹 LIMPIANDO BASE DE DATOS")
    print("=" * 50)
    
    # Orden de eliminación para evitar conflictos de claves foráneas
    models_to_clear = [
        # Seguridad
        ('AccesoVehiculo', AccesoVehiculo),
        ('Visita', Visita),
        ('RegistroAcceso', RegistroAcceso),
        ('VehiculoAutorizado', VehiculoAutorizado),
        ('Incidente', Incidente),
        
        # Reservas
        ('Reserva', Reserva),
        ('EspacioComun', EspacioComun),
        
        # Comunicación
        ('Respuesta', Respuesta),
        ('Comunicado', Comunicado),
        ('Notificacion', Notificacion),
        
        # Mantenimiento
        ('SolicitudMantenimiento', SolicitudMantenimiento),
        
        # Finanzas
        ('AnalisisMorosidad', AnalisisMorosidad),
        ('Multa', Multa),
        ('Pago', Pago),
        ('CuentaCobrar', CuentaCobrar),
        ('TipoPago', TipoPago),
        
        # Unidades
        ('UnidadHabitacional', UnidadHabitacional),
        
        # Usuarios
        ('PerfilUsuario', PerfilUsuario),
        ('Usuario', Usuario),
    ]
    
    total_deleted = 0
    
    for model_name, model_class in models_to_clear:
        try:
            count = model_class.objects.count()
            if count > 0:
                deleted_count = model_class.objects.all().delete()[0]
                total_deleted += deleted_count
                print(f"✅ {model_name}: {deleted_count} registros eliminados")
            else:
                print(f"⚪ {model_name}: Sin registros para eliminar")
        except Exception as e:
            print(f"❌ Error eliminando {model_name}: {str(e)}")
    
    # Limpiar grupos (excepto los grupos por defecto que podrían recrearse)
    try:
        groups_count = Group.objects.exclude(name__in=['Administradores', 'Residentes', 'Seguridad', 'Mantenimiento']).count()
        if groups_count > 0:
            deleted_groups = Group.objects.exclude(name__in=['Administradores', 'Residentes', 'Seguridad', 'Mantenimiento']).delete()[0]
            total_deleted += deleted_groups
            print(f"✅ Grupos adicionales: {deleted_groups} eliminados")
    except Exception as e:
        print(f"❌ Error eliminando grupos: {str(e)}")
    
    print(f"\n🎯 RESUMEN: {total_deleted} registros eliminados en total")
    print("✅ Base de datos limpia y lista para nueva población")

if __name__ == '__main__':
    clear_all_data()