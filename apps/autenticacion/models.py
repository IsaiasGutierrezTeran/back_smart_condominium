from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuarios"

class PerfilUsuario(models.Model):
    ROLES = (
        ('residente', 'Residente'),
        ('administrador', 'Administrador'),
        ('seguridad', 'Seguridad'),
        ('mantenimiento', 'Mantenimiento'),
    )
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil', verbose_name="Usuario")
    rol = models.CharField(max_length=20, choices=ROLES, default='residente', verbose_name="Rol")
    numero_unidad = models.CharField(max_length=10, blank=True, verbose_name="Número de Unidad")
    edificio = models.CharField(max_length=10, blank=True, verbose_name="Edificio")
    avatar = models.ImageField(upload_to='avatares/', blank=True, verbose_name="Foto de Perfil")
    contacto_emergencia = models.CharField(max_length=100, blank=True, verbose_name="Contacto de Emergencia")
    es_propietario = models.BooleanField(default=True, verbose_name="Es Propietario")
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        db_table = "perfiles_usuarios"
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_rol_display()}"