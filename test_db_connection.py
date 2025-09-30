#!/usr/bin/env python3
"""
Script para probar la conexión directa a la base de datos de Render
"""
import psycopg2
import sys

# Datos de conexión de Render
DB_HOST = "dpg-d3dh76gjchc7a13bu0-a.oregon-postgres.render.com"
DB_PORT = "5432"
DB_NAME = "condominiobd"
DB_USER = "condominiobd_user"
DB_PASSWORD = "6rfi72dVJ42xm7OImtCNsrx1lO2wGyov"

print("🔍 PROBANDO CONEXIÓN A RENDER...")
print(f"Host: {DB_HOST}")
print(f"Puerto: {DB_PORT}")
print(f"Base de datos: {DB_NAME}")
print(f"Usuario: {DB_USER}")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# Diferentes configuraciones SSL para probar
ssl_configs = [
    {"sslmode": "require"},
    {"sslmode": "prefer"},
    {"sslmode": "allow"},
    {"sslmode": "disable"},
    {},  # Sin SSL
]

for i, ssl_config in enumerate(ssl_configs, 1):
    print(f"\n🧪 PRUEBA {i}: SSL Config = {ssl_config if ssl_config else 'Sin SSL'}")
    
    try:
        # Intentar conexión
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            **ssl_config
        )
        
        # Si llegamos aquí, la conexión fue exitosa
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ ¡CONEXIÓN EXITOSA!")
        print(f"   PostgreSQL Version: {version[0][:50]}...")
        
        cursor.close()
        conn.close()
        
        print(f"🎯 CONFIGURACIÓN QUE FUNCIONA: {ssl_config}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        break
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error: {str(e)[:100]}...")
        
    except Exception as e:
        print(f"💥 Error inesperado: {str(e)}")

else:
    print("\n😞 NINGUNA CONFIGURACIÓN FUNCIONÓ")
    print("Posibles problemas:")
    print("1. Firewall bloqueando conexiones externas")
    print("2. Credenciales incorrectas")
    print("3. Base de datos no disponible")
    print("4. Problema de red/ISP")

print("\n🔧 ALTERNATIVAS:")
print("1. Usar Django Admin desde el backend desplegado en Render")
print("2. Crear una base de datos local para desarrollo")
print("3. Usar túnel SSH si Render lo permite")