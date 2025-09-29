#!/usr/bin/env python
"""
Script para limpiar triggers problemáticos en la base de datos
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_condominium.settings.base')

# Setup Django
django.setup()

from django.db import connection

def clean_database_triggers():
    """Limpiar triggers problemáticos"""
    print("🧹 Limpiando triggers problemáticos...")
    
    with connection.cursor() as cursor:
        # Listar todos los triggers
        cursor.execute("""
            SELECT trigger_name, event_object_table 
            FROM information_schema.triggers 
            WHERE trigger_schema = 'public'
        """)
        triggers = cursor.fetchall()
        
        print(f"Encontrados {len(triggers)} triggers:")
        
        for trigger_name, table_name in triggers:
            print(f"  - {trigger_name} en tabla {table_name}")
            
            # Eliminar trigger
            try:
                cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name} ON {table_name} CASCADE")
                print(f"    ✅ Eliminado")
            except Exception as e:
                print(f"    ❌ Error eliminando: {e}")
        
        # Eliminar funciones relacionadas
        cursor.execute("""
            SELECT routine_name 
            FROM information_schema.routines 
            WHERE routine_schema = 'public' 
            AND routine_type = 'FUNCTION'
            AND routine_name LIKE '%fecha%' OR routine_name LIKE '%timestamp%'
        """)
        functions = cursor.fetchall()
        
        print(f"\nEncontradas {len(functions)} funciones relacionadas:")
        
        for (function_name,) in functions:
            print(f"  - {function_name}")
            
            try:
                cursor.execute(f"DROP FUNCTION IF EXISTS {function_name}() CASCADE")
                print(f"    ✅ Eliminada")
            except Exception as e:
                print(f"    ❌ Error eliminando: {e}")

if __name__ == "__main__":
    try:
        clean_database_triggers()
        print("\n✅ Limpieza completada. Ahora puedes ejecutar populate_database.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()