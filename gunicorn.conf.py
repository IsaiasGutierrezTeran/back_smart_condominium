"""
Configuración de Gunicorn para Render
"""
import os

# Configuración básica
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get('WEB_CONCURRENCY', '4'))

# Configuración de worker
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Configuración de archivos
max_requests = 1000
max_requests_jitter = 100

# Configuración de logs
loglevel = "info"
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Configuración de aplicación
wsgi_module = "smart_condominium.wsgi:application"

# Preload para mejor rendimiento
preload_app = True

# Configuración de seguridad
forwarded_allow_ips = "*"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}