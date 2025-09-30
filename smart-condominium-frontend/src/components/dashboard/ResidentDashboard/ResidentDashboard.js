// Smart Condominium - Dashboard de Residente
import React from 'react';
import { Grid, Card, CardContent, Typography, Box, Button, Chip } from '@mui/material';
import {
  AccountBalanceWallet,
  EventAvailable,
  Notifications,
  Build,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

import MetricCard from '../MetricCard/MetricCard';

const ResidentDashboard = () => {
  const metrics = [
    {
      title: 'Saldo Pendiente',
      value: '$280',
      change: 'Vence en 5 días',
      changeType: 'warning',
      icon: <AccountBalanceWallet />,
      color: 'warning',
    },
    {
      title: 'Reservas Activas',
      value: '2',
      change: 'Próxima: Salón',
      changeType: 'positive',
      icon: <EventAvailable />,
      color: 'success',
    },
    {
      title: 'Notificaciones',
      value: '5',
      change: '2 nuevas',
      changeType: 'neutral',
      icon: <Notifications />,
      color: 'info',
    },
    {
      title: 'Mantenimientos',
      value: '1',
      change: 'En progreso',
      changeType: 'neutral',
      icon: <Build />,
      color: 'primary',
    },
  ];

  const quickActions = [
    { title: 'Pagar Cuota', description: 'Pago mensual de mantenimiento', action: 'Ver detalles' },
    { title: 'Reservar Espacio', description: 'Salón de eventos, gimnasio, etc.', action: 'Reservar' },
    { title: 'Reportar Problema', description: 'Solicitud de mantenimiento', action: 'Reportar' },
  ];

  const recentNotifications = [
    {
      id: 1,
      title: 'Pago vencido',
      description: 'Su cuota de mantenimiento está vencida',
      time: 'Hace 2 días',
      type: 'error',
    },
    {
      id: 2,
      title: 'Reserva aprobada',
      description: 'Su reserva del salón de eventos fue aprobada',
      time: 'Hace 1 día',
      type: 'success',
    },
    {
      id: 3,
      title: 'Mantenimiento programado',
      description: 'Mantenimiento de ascensores mañana 9:00 AM',
      time: 'Hace 3 horas',
      type: 'info',
    },
  ];

  return (
    <Box>
      {/* Métricas principales */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {metrics.map((metric, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <MetricCard {...metric} />
            </motion.div>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Acciones rápidas */}
        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2" sx={{ mb: 3 }}>
                  Acciones Rápidas
                </Typography>
                <Grid container spacing={2}>
                  {quickActions.map((action, index) => (
                    <Grid item xs={12} sm={4} key={index}>
                      <Card variant="outlined" sx={{ height: '100%' }}>
                        <CardContent>
                          <Typography variant="h6" component="h3" gutterBottom>
                            {action.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {action.description}
                          </Typography>
                          <Button variant="outlined" size="small" fullWidth>
                            {action.action}
                          </Button>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Notificaciones recientes */}
        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
                  Notificaciones Recientes
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {recentNotifications.map((notification) => (
                    <Box
                      key={notification.id}
                      sx={{
                        p: 2,
                        backgroundColor: 'grey.50',
                        borderRadius: 1,
                        borderLeft: 4,
                        borderLeftColor: `${notification.type}.main`,
                      }}
                    >
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {notification.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {notification.description}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {notification.time}
                      </Typography>
                    </Box>
                  ))}
                </Box>
                <Button variant="text" size="small" fullWidth sx={{ mt: 2 }}>
                  Ver todas las notificaciones
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ResidentDashboard;