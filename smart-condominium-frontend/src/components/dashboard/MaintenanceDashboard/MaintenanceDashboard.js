// Smart Condominium - Dashboard de Mantenimiento
import React from 'react';
import { Grid, Card, CardContent, Typography, Box, List, ListItem, ListItemText, Chip } from '@mui/material';
import {
  Build,
  Assignment,
  Schedule,
  CheckCircle,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

import MetricCard from '../MetricCard/MetricCard';

const MaintenanceDashboard = () => {
  const metrics = [
    {
      title: 'Solicitudes Pendientes',
      value: '8',
      change: '+2 hoy',
      changeType: 'neutral',
      icon: <Assignment />,
      color: 'warning',
    },
    {
      title: 'En Progreso',
      value: '3',
      change: '2 programadas',
      changeType: 'positive',
      icon: <Schedule />,
      color: 'info',
    },
    {
      title: 'Completadas Hoy',
      value: '5',
      change: '+2 vs ayer',
      changeType: 'positive',
      icon: <CheckCircle />,
      color: 'success',
    },
    {
      title: 'Herramientas',
      value: '12',
      change: 'Disponibles',
      changeType: 'neutral',
      icon: <Build />,
      color: 'primary',
    },
  ];

  const pendingRequests = [
    { 
      id: 1, 
      title: 'Fuga en tubería', 
      location: 'Apto 301', 
      priority: 'Alta', 
      time: '2 horas',
      assignedTo: 'Juan Pérez'
    },
    { 
      id: 2, 
      title: 'Luz fundida', 
      location: 'Pasillo Piso 5', 
      priority: 'Media', 
      time: '4 horas',
      assignedTo: 'No asignado'
    },
    { 
      id: 3, 
      title: 'Aire acondicionado', 
      location: 'Apto 205', 
      priority: 'Baja', 
      time: '1 día',
      assignedTo: 'Carlos López'
    },
  ];

  const scheduledTasks = [
    {
      id: 1,
      title: 'Mantenimiento ascensores',
      time: '09:00 - 12:00',
      status: 'Programado',
      technician: 'Equipo A',
    },
    {
      id: 2,
      title: 'Revisión sistema eléctrico',
      time: '14:00 - 16:00',
      status: 'En progreso',
      technician: 'María González',
    },
    {
      id: 3,
      title: 'Limpieza tanques de agua',
      time: '08:00 - 10:00 (Mañana)',
      status: 'Programado',
      technician: 'Equipo B',
    },
  ];

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'alta':
        return 'error';
      case 'media':
        return 'warning';
      case 'baja':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'programado':
        return 'info';
      case 'en progreso':
        return 'warning';
      case 'completado':
        return 'success';
      default:
        return 'default';
    }
  };

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
        {/* Solicitudes pendientes */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
                  Solicitudes Pendientes
                </Typography>
                <List>
                  {pendingRequests.map((request) => (
                    <ListItem key={request.id} divider>
                      <ListItemText
                        primary={request.title}
                        secondary={
                          <Box>
                            <Typography variant="caption" display="block">
                              {request.location} - Hace {request.time}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              Asignado a: {request.assignedTo}
                            </Typography>
                          </Box>
                        }
                      />
                      <Chip
                        label={request.priority}
                        size="small"
                        color={getPriorityColor(request.priority)}
                        variant="outlined"
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Tareas programadas */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
                  Tareas Programadas
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {scheduledTasks.map((task) => (
                    <Box
                      key={task.id}
                      sx={{
                        p: 2,
                        backgroundColor: 'grey.50',
                        borderRadius: 1,
                        borderLeft: 4,
                        borderLeftColor: `${getStatusColor(task.status)}.main`,
                      }}
                    >
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                          {task.title}
                        </Typography>
                        <Chip
                          label={task.status}
                          size="small"
                          color={getStatusColor(task.status)}
                          variant="outlined"
                        />
                      </Box>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {task.time}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Asignado a: {task.technician}
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

export default MaintenanceDashboard;