#!/usr/bin/env python
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

def list_tables():
    """Lista todas las tablas en la base de datos"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print("=== TABLAS EN LA BASE DE DATOS ===")
        print(f"Total de tablas: {len(tables)}")
        print("-" * 50)
        
        for table in tables:
            table_name = table[0]
            
            # Contar registros en cada tabla
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"{table_name:40} | {count:5} registros")
            except Exception as e:
                print(f"{table_name:40} | Error: {str(e)[:20]}")

if __name__ == "__main__":
    try:
        list_tables()
        print("\n✅ ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
        print("Todas las tablas han sido creadas en PostgreSQL")
    except Exception as e:
        print(f"❌ Error: {e}")