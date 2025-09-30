// Smart Condominium - Dashboard Principal
import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import { motion } from 'framer-motion';

import { useAuth } from '../contexts/AuthContext';
import AdminDashboard from '../components/dashboard/AdminDashboard/AdminDashboard';
import ResidentDashboard from '../components/dashboard/ResidentDashboard/ResidentDashboard';
import SecurityDashboard from '../components/dashboard/SecurityDashboard/SecurityDashboard';
import MaintenanceDashboard from '../components/dashboard/MaintenanceDashboard/MaintenanceDashboard';

const Dashboard = () => {
  const { user, getUserRole } = useAuth();
  const userRole = getUserRole();

  const getDashboardComponent = () => {
    switch (userRole) {
      case 'administrador':
        return <AdminDashboard />;
      case 'residente':
        return <ResidentDashboard />;
      case 'seguridad':
        return <SecurityDashboard />;
      case 'mantenimiento':
        return <MaintenanceDashboard />;
      default:
        return <ResidentDashboard />;
    }
  };

  const getWelcomeMessage = () => {
    const roleMessages = {
      administrador: '¡Bienvenido al panel de administración!',
      residente: '¡Bienvenido a su hogar inteligente!',
      seguridad: '¡Bienvenido al centro de seguridad!',
      mantenimiento: '¡Bienvenido al centro de mantenimiento!',
    };
    
    return roleMessages[userRole] || '¡Bienvenido!';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
          {getWelcomeMessage()}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          {user && `${user.first_name} ${user.last_name}`} - 
          {userRole && ` ${userRole.charAt(0).toUpperCase() + userRole.slice(1)}`}
        </Typography>
      </Box>

      {getDashboardComponent()}
    </motion.div>
  );
};

export default Dashboard;