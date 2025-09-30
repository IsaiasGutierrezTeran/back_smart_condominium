// Smart Condominium - Página principal de Seguridad
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Typography, Box } from '@mui/material';
import { motion } from 'framer-motion';

const SecurityPage = () => {
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
                Módulo de Seguridad
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Control de acceso, visitantes, vehículos e incidentes de seguridad.
              </Typography>
            </Box>
          }
        />
        <Route path="visitors" element={<div>Gestión de Visitantes</div>} />
        <Route path="vehicles" element={<div>Control Vehicular</div>} />
        <Route path="incidents" element={<div>Incidentes de Seguridad</div>} />
        <Route path="access" element={<div>Control de Acceso</div>} />
        <Route path="reports" element={<div>Reportes de Seguridad</div>} />
        <Route path="*" element={<Navigate to="/security" replace />} />
      </Routes>
    </motion.div>
  );
};

export default SecurityPage;