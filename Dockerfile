FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=smart_condominium.settings.production

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        libc6-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para archivos estáticos
RUN mkdir -p staticfiles

# Crear directorio para logs y dar permisos
RUN mkdir -p /var/log/django && chmod 777 /var/log/django

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput --settings=smart_condominium.settings.production

# Copiar scripts y dar permisos
COPY entrypoint.sh /entrypoint.sh
COPY load_initial_data.py /app/load_initial_data.py
RUN chmod +x /entrypoint.sh
RUN chmod +x /app/load_initial_data.py

# Crear usuario no-root
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app && chown -R appuser /var/log/django
USER appuser

# Exponer puerto
EXPOSE 8000

# Comando de inicio
ENTRYPOINT ["/entrypoint.sh"]