// Smart Condominium - Página principal de Comunicación
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Typography, Box } from '@mui/material';
import { motion } from 'framer-motion';

const CommunicationPage = () => {
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
                Módulo de Comunicación
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Noticias, avisos y notificaciones del condominio.
              </Typography>
            </Box>
          }
        />
        <Route path="news" element={<div>Noticias</div>} />
        <Route path="announcements" element={<div>Avisos</div>} />
        <Route path="manage" element={<div>Gestionar Comunicación</div>} />
        <Route path="*" element={<Navigate to="/communication" replace />} />
      </Routes>
    </motion.div>
  );
};

export default CommunicationPage;