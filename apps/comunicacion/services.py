from django.db.models import Q
from django.utils import timezone
from .models import Notificacion, DestinatarioNotificacion, ConfiguracionNotificacion
from apps.autenticacion.models import Usuario
from apps.finanzas.models import UnidadHabitacional
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """
    Servicio para envío y gestión de notificaciones
    """
    
    @staticmethod
    def obtener_destinatarios(notificacion):
        """
        Obtener lista de usuarios destinatarios según el tipo de destinatario
        """
        usuarios = []
        
        if notificacion.tipo_destinatario == 'todos':
            usuarios = Usuario.objects.filter(is_active=True)
            
        elif notificacion.tipo_destinatario == 'residentes':
            usuarios = Usuario.objects.filter(
                Q(unidades_propias__isnull=False) | Q(unidades_alquiladas__isnull=False),
                is_active=True
            ).distinct()
            
        elif notificacion.tipo_destinatario == 'propietarios':
            usuarios = Usuario.objects.filter(
                unidades_propias__isnull=False,
                is_active=True
            ).distinct()
            
        elif notificacion.tipo_destinatario == 'inquilinos':
            usuarios = Usuario.objects.filter(
                unidades_alquiladas__isnull=False,
                is_active=True
            ).distinct()
            
        elif notificacion.tipo_destinatario == 'administradores':
            usuarios = Usuario.objects.filter(
                Q(is_staff=True) | Q(perfil__rol='administrador'),
                is_active=True
            )
            
        elif notificacion.tipo_destinatario == 'seguridad':
            usuarios = Usuario.objects.filter(
                perfil__rol='seguridad',
                is_active=True
            )
            
        elif notificacion.tipo_destinatario == 'mantenimiento':
            usuarios = Usuario.objects.filter(
                perfil__rol='mantenimiento',
                is_active=True
            )
            
        elif notificacion.tipo_destinatario == 'edificio':
            if notificacion.edificios_objetivo:
                unidades = UnidadHabitacional.objects.filter(
                    edificio__in=notificacion.edificios_objetivo
                )
                usuarios_propietarios = Usuario.objects.filter(
                    unidades_propias__in=unidades,
                    is_active=True
                ).distinct()
                usuarios_inquilinos = Usuario.objects.filter(
                    unidades_alquiladas__in=unidades,
                    is_active=True
                ).distinct()
                usuarios = usuarios_propietarios.union(usuarios_inquilinos)
            
        elif notificacion.tipo_destinatario == 'unidades':
            if notificacion.unidades_objetivo:
                unidades = UnidadHabitacional.objects.filter(
                    id__in=notificacion.unidades_objetivo
                )
                usuarios_propietarios = Usuario.objects.filter(
                    unidades_propias__in=unidades,
                    is_active=True
                ).distinct()
                usuarios_inquilinos = Usuario.objects.filter(
                    unidades_alquiladas__in=unidades,
                    is_active=True
                ).distinct()
                usuarios = usuarios_propietarios.union(usuarios_inquilinos)
                
        elif notificacion.tipo_destinatario == 'usuarios':
            # Los usuarios específicos ya están en la relación ManyToMany
            usuarios = notificacion.usuarios_especificos.filter(is_active=True)
        
        return usuarios
    
    @staticmethod
    def enviar_notificacion(notificacion):
        """
        Procesar y enviar una notificación
        """
        try:
            # Validar que esté en estado correcto
            if notificacion.estado != 'borrador':
                raise ValueError(f"No se puede enviar notificación en estado {notificacion.estado}")
            
            # Obtener destinatarios
            usuarios_destinatarios = NotificationService.obtener_destinatarios(notificacion)
            
            # Crear registros de destinatarios
            destinatarios_creados = []
            errores = []
            
            for usuario in usuarios_destinatarios:
                try:
                    # Verificar configuración del usuario
                    config = getattr(usuario, 'config_notificaciones', None)
                    if config and not NotificationService.puede_recibir_notificacion(config, notificacion):
                        continue
                    
                    destinatario, created = DestinatarioNotificacion.objects.get_or_create(
                        notificacion=notificacion,
                        usuario=usuario,
                        defaults={'estado': 'enviado', 'fecha_envio': timezone.now()}
                    )
                    
                    if created or destinatario.estado == 'no_enviado':
                        # Enviar notificación según los canales configurados
                        if notificacion.es_push and config and config.recibir_push:
                            NotificationService.enviar_push(destinatario)
                        
                        if notificacion.es_email and config and config.recibir_email:
                            NotificationService.enviar_email(destinatario)
                        
                        if notificacion.es_sms and config and config.recibir_sms:
                            NotificationService.enviar_sms(destinatario)
                        
                        destinatario.estado = 'enviado'
                        destinatario.fecha_envio = timezone.now()
                        destinatario.save()
                        destinatarios_creados.append(destinatario)
                
                except Exception as e:
                    logger.error(f"Error enviando a usuario {usuario.id}: {e}")
                    errores.append(f"Usuario {usuario.email}: {str(e)}")
            
            # Actualizar estadísticas de la notificación
            notificacion.total_destinatarios = len(destinatarios_creados)
            notificacion.total_enviados = len(destinatarios_creados)
            notificacion.estado = 'enviada'
            notificacion.fecha_envio = timezone.now()
            notificacion.save()
            
            return {
                'total_destinatarios': len(destinatarios_creados),
                'enviados_exitosos': len(destinatarios_creados),
                'errores': errores
            }
            
        except Exception as e:
            logger.error(f"Error enviando notificación {notificacion.id}: {e}")
            notificacion.estado = 'cancelada'
            notificacion.save()
            raise e
    
    @staticmethod
    def puede_recibir_notificacion(config, notificacion):
        """
        Verificar si el usuario puede recibir la notificación según su configuración
        """
        # Verificar horario
        now = timezone.now()
        hora_actual = now.time()
        
        if not (config.horario_inicio <= hora_actual <= config.horario_fin):
            # Solo permitir notificaciones urgentes fuera del horario
            if not notificacion.es_urgente:
                return False
        
        # Verificar fin de semana
        if config.no_molestar_fines_semana and now.weekday() >= 5:  # Sábado y Domingo
            if not notificacion.es_urgente:
                return False
        
        # Verificar configuraciones por categoría
        categoria_nombre = notificacion.categoria.nombre.lower()
        
        if 'pago' in categoria_nombre and not config.notif_pagos:
            return False
        elif 'mantenimiento' in categoria_nombre and not config.notif_mantenimiento:
            return False
        elif 'seguridad' in categoria_nombre and not config.notif_seguridad:
            return False
        elif 'evento' in categoria_nombre and not config.notif_eventos:
            return False
        elif 'aviso' in categoria_nombre and not config.notif_avisos:
            return False
        elif 'reserva' in categoria_nombre and not config.notif_reservas:
            return False
        
        return True
    
    @staticmethod
    def enviar_push(destinatario):
        """
        Enviar notificación push (integración con FCM)
        """
        try:
            config = destinatario.usuario.config_notificaciones
            tokens = []
            
            if config.token_fcm_android:
                tokens.append(config.token_fcm_android)
            if config.token_fcm_ios:
                tokens.append(config.token_fcm_ios)
            if config.token_fcm_web:
                tokens.append(config.token_fcm_web)
            
            if not tokens:
                return False
            
            # Aquí iría la integración real con Firebase Cloud Messaging
            # Por ahora solo simulamos el envío
            logger.info(f"Push enviado a {destinatario.usuario.email}")
            
            # Actualizar estado
            destinatario.fecha_entrega = timezone.now()
            if destinatario.estado == 'enviado':
                destinatario.estado = 'entregado'
            destinatario.save()
            
            return True
            
        except Exception as e:
            logger.error(f"Error enviando push a {destinatario.usuario.email}: {e}")
            destinatario.estado = 'error'
            destinatario.mensaje_error = str(e)
            destinatario.save()
            return False
    
    @staticmethod
    def enviar_email(destinatario):
        """
        Enviar notificación por email
        """
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            notificacion = destinatario.notificacion
            
            asunto = notificacion.titulo
            mensaje = f"""
            Estimado/a {destinatario.usuario.get_full_name()},
            
            {notificacion.mensaje}
            
            ---
            Condominio Inteligente
            Sistema de Notificaciones
            """
            
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [destinatario.usuario.email],
                fail_silently=False,
            )
            
            logger.info(f"Email enviado a {destinatario.usuario.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando email a {destinatario.usuario.email}: {e}")
            destinatario.estado = 'error'
            destinatario.mensaje_error = str(e)
            destinatario.save()
            return False
    
    @staticmethod
    def enviar_sms(destinatario):
        """
        Enviar notificación por SMS (integración con proveedor SMS)
        """
        try:
            if not destinatario.usuario.telefono:
                return False
            
            # Aquí iría la integración real con un proveedor SMS
            # Por ahora solo simulamos el envío
            logger.info(f"SMS enviado a {destinatario.usuario.telefono}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando SMS a {destinatario.usuario.telefono}: {e}")
            return False