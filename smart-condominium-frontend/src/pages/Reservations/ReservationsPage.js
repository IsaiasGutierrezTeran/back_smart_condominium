// Smart Condominium - Página principal de Reservas
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Typography, Box } from '@mui/material';
import { motion } from 'framer-motion';

const ReservationsPage = () => {
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
                Módulo de Reservas
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Reserva de espacios comunes y gestión de disponibilidad.
              </Typography>
            </Box>
          }
        />
        <Route path="book" element={<div>Hacer Reserva</div>} />
        <Route path="my-reservations" element={<div>Mis Reservas</div>} />
        <Route path="spaces" element={<div>Espacios Disponibles</div>} />
        <Route path="manage" element={<div>Administrar Reservas</div>} />
        <Route path="*" element={<Navigate to="/reservations" replace />} />
      </Routes>
    </motion.div>
  );
};

export default ReservationsPage;