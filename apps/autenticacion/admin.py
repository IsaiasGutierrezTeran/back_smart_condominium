from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PerfilUsuario

@admin.register(Usuario)
class AdminUsuario(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('telefono',)}),
    )

@admin.register(PerfilUsuario)
class AdminPerfilUsuario(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'numero_unidad', 'edificio', 'es_propietario')
    list_filter = ('rol', 'es_propietario', 'edificio')
    search_fields = ('usuario__email', 'usuario__first_name', 'numero_unidad')
    ordering = ('usuario__email',)