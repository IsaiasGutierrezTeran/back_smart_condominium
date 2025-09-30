// Smart Condominium - Dashboard de Seguridad
import React from 'react';
import { Grid, Card, CardContent, Typography, Box, List, ListItem, ListItemText, Chip } from '@mui/material';
import {
  Security,
  People,
  DirectionsCar,
  Warning,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

import MetricCard from '../MetricCard/MetricCard';

const SecurityDashboard = () => {
  const metrics = [
    {
      title: 'Visitantes Hoy',
      value: '12',
      change: '+3 vs ayer',
      changeType: 'positive',
      icon: <People />,
      color: 'primary',
    },
    {
      title: 'En el Edificio',
      value: '8',
      change: '4 esperados',
      changeType: 'neutral',
      icon: <Security />,
      color: 'success',
    },
    {
      title: 'Vehículos',
      value: '5',
      change: 'Ingresados hoy',
      changeType: 'neutral',
      icon: <DirectionsCar />,
      color: 'info',
    },
    {
      title: 'Incidentes',
      value: '1',
      change: 'Abierto',
      changeType: 'warning',
      icon: <Warning />,
      color: 'warning',
    },
  ];

  const todayVisitors = [
    { name: 'María González', resident: 'Apto 301', time: '09:30', status: 'En visita' },
    { name: 'Carlos López', resident: 'Apto 205', time: '10:15', status: 'Salió' },
    { name: 'Ana Martínez', resident: 'Apto 402', time: '11:00', status: 'En visita' },
    { name: 'Luis Fernández', resident: 'Apto 150', time: '12:30', status: 'En visita' },
  ];

  const recentIncidents = [
    {
      id: 1,
      title: 'Ruido excesivo',
      location: 'Torre B - Piso 8',
      time: '14:30',
      status: 'En investigación',
      severity: 'media',
    },
    {
      id: 2,
      title: 'Vehículo no autorizado',
      location: 'Estacionamiento A',
      time: '13:15',
      status: 'Resuelto',
      severity: 'baja',
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
        {/* Visitantes del día */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
                  Visitantes del Día
                </Typography>
                <List>
                  {todayVisitors.map((visitor, index) => (
                    <ListItem key={index} divider={index < todayVisitors.length - 1}>
                      <ListItemText
                        primary={visitor.name}
                        secondary={`${visitor.resident} - ${visitor.time}`}
                      />
                      <Chip
                        label={visitor.status}
                        size="small"
                        color={visitor.status === 'En visita' ? 'success' : 'default'}
                        variant="outlined"
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Incidentes recientes */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
                  Incidentes Recientes
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {recentIncidents.map((incident) => (
                    <Box
                      key={incident.id}
                      sx={{
                        p: 2,
                        backgroundColor: 'grey.50',
                        borderRadius: 1,
                        borderLeft: 4,
                        borderLeftColor: incident.severity === 'alta' ? 'error.main' : 
                                       incident.severity === 'media' ? 'warning.main' : 'info.main',
                      }}
                    >
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                          {incident.title}
                        </Typography>
                        <Chip
                          label={incident.status}
                          size="small"
                          color={incident.status === 'Resuelto' ? 'success' : 'warning'}
                          variant="outlined"
                        />
                      </Box>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {incident.location}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {incident.time}
                      </Typography>
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

export default SecurityDashboard;