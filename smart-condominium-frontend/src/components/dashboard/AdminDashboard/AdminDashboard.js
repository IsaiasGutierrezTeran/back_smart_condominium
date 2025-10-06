// Smart Condominium - Dashboard de Administrador
import React from 'react';
import { Grid, Card, CardContent, Typography, Box, IconButton } from '@mui/material';
import {
  People,
  AccountBalanceWallet,
  Security,
  Build,
  TrendingUp,
  Warning,
  CheckCircle,
  MoreVert,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

import MetricCard from '../MetricCard/MetricCard';

const AdminDashboard = () => {
  const metrics = [
    {
      title: 'Total Residentes',
      value: '156',
      change: '+12%',
      changeType: 'positive',
      icon: <People />,
      color: 'primary',
    },
    {
      title: 'Ingresos del Mes',
      value: '$45,280',
      change: '+8.2%',
      changeType: 'positive',
      icon: <AccountBalanceWallet />,
      color: 'success',
    },
    {
      title: 'Incidentes Abiertos',
      value: '3',
      change: '-2',
      changeType: 'negative',
      icon: <Security />,
      color: 'warning',
    },
    {
      title: 'Mantenimientos',
      value: '8',
      change: '+3',
      changeType: 'neutral',
      icon: <Build />,
      color: 'info',
    },
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'payment',
      title: 'Pago recibido',
      description: 'Juan Pérez - Apto 301 - $280',
      time: 'Hace 5 min',
      icon: <CheckCircle color="success" />,
    },
    {
      id: 2,
      type: 'security',
      title: 'Incidente reportado',
      description: 'Ruido excesivo - Torre B',
      time: 'Hace 15 min',
      icon: <Warning color="warning" />,
    },
    {
      id: 3,
      type: 'maintenance',
      title: 'Mantenimiento completado',
      description: 'Reparación ascensor 2',
      time: 'Hace 1 hora',
      icon: <Build color="info" />,
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
        {/* Gráfico de tendencias */}
        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6" component="h2">
                    Tendencia de Ingresos
                  </Typography>
                  <IconButton size="small">
                    <MoreVert />
                  </IconButton>
                </Box>
                <Box sx={{ 
                  height: 300, 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  backgroundColor: 'grey.50',
                  borderRadius: 1,
                }}>
                  <TrendingUp sx={{ fontSize: 48, color: 'text.secondary' }} />
                  <Typography variant="body1" color="text.secondary" sx={{ ml: 2 }}>
                    Gráfico de tendencias aquí
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Actividad reciente */}
        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
                  Actividad Reciente
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {recentActivities.map((activity) => (
                    <Box
                      key={activity.id}
                      sx={{
                        display: 'flex',
                        alignItems: 'flex-start',
                        gap: 2,
                        p: 2,
                        backgroundColor: 'grey.50',
                        borderRadius: 1,
                      }}
                    >
                      <Box sx={{ mt: 0.5 }}>
                        {activity.icon}
                      </Box>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                          {activity.title}
                        </Typography>
                        <Typography variant="caption" color="text.secondary" display="block">
                          {activity.description}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {activity.time}
                        </Typography>
                      </Box>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AdminDashboard;