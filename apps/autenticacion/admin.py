from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PerfilUsuario

@admin.register(Usuario)
class AdminUsuario(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Configurar fieldsets para el modelo personalizado
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'telefono')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'telefono'),
        }),
    )
    
    # Configurar el username automáticamente
    def save_model(self, request, obj, form, change):
        if not change:  # Solo para nuevos usuarios
            obj.username = obj.email
        super().save_model(request, obj, form, change)

@admin.register(PerfilUsuario)
class AdminPerfilUsuario(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'numero_unidad', 'edificio', 'es_propietario')
    list_filter = ('rol', 'es_propietario', 'edificio')
    search_fields = ('usuario__email', 'usuario__first_name', 'numero_unidad')
    ordering = ('usuario__email',)