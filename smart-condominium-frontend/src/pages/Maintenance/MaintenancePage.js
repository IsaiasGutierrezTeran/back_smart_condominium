// Smart Condominium - Página principal de Mantenimiento
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Typography, Box } from '@mui/material';
import { motion } from 'framer-motion';

const MaintenancePage = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Routes>
        <Route
          index
          element={
            <Box>
              <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
                Módulo de Mantenimiento
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Gestión de solicitudes de mantenimiento y seguimiento de trabajos.
              </Typography>
            </Box>
          }
        />
        <Route path="requests" element={<div>Nueva Solicitud</div>} />
        <Route path="my-requests" element={<div>Mis Solicitudes</div>} />
        <Route path="manage" element={<div>Gestionar Mantenimiento</div>} />
        <Route path="reports" element={<div>Reportes de Mantenimiento</div>} />
        <Route path="*" element={<Navigate to="/maintenance" replace />} />
      </Routes>
    </motion.div>
  );
};

export default MaintenancePage;