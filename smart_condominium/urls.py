from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.autenticacion.urls')),
    path('api/finanzas/', include('apps.finanzas.urls')),
    path('api/comunicacion/', include('apps.comunicacion.urls')),
    path('api/reservas/', include('apps.reservas.urls')),
    path('api/seguridad/', include('apps.seguridad.urls')),
    path('api/mantenimiento/', include('apps.mantenimiento.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)