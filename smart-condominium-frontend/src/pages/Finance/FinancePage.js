// Smart Condominium - Página principal de Finanzas
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Typography, Box } from '@mui/material';
import { motion } from 'framer-motion';

const FinancePage = () => {
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
                Módulo de Finanzas
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Gestión de pagos, cuotas y reportes financieros del condominio.
              </Typography>
            </Box>
          }
        />
        <Route path="payments" element={<div>Mis Pagos</div>} />
        <Route path="history" element={<div>Historial de Pagos</div>} />
        <Route path="admin" element={<div>Administrar Finanzas</div>} />
        <Route path="reports" element={<div>Reportes Financieros</div>} />
        <Route path="*" element={<Navigate to="/finance" replace />} />
      </Routes>
    </motion.div>
  );
};

export default FinancePage;