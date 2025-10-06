// Smart Condominium - Aplicación principal
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';

import { useAuth } from './contexts/AuthContext';
import Layout from './components/common/Layout/Layout';
import LoadingSpinner from './components/common/LoadingSpinner/LoadingSpinner';
import ProtectedRoute from './components/auth/ProtectedRoute/ProtectedRoute';

// Páginas públicas
import Login from './pages/Login';
import Register from './pages/Register';

// Páginas protegidas
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

// Páginas de módulos
import FinancePage from './pages/Finance/FinancePage';
import CommunicationPage from './pages/Communication/CommunicationPage';
import ReservationsPage from './pages/Reservations/ReservationsPage';
import SecurityPage from './pages/Security/SecurityPage';
import MaintenancePage from './pages/Maintenance/MaintenancePage';

function App() {
  const { loading, isAuthenticated } = useAuth();

  // Mostrar spinner mientras se verifica la autenticación
  if (loading) {
    return (
      <Box className="full-height flex-center">
        <LoadingSpinner size={60} />
      </Box>
    );
  }

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Routes>
        {/* Rutas públicas */}
        <Route
          path="/login"
          element={
            !isAuthenticated ? (
              <Login />
            ) : (
              <Navigate to="/dashboard" replace />
            )
          }
        />
        <Route
          path="/register"
          element={
            !isAuthenticated ? (
              <Register />
            ) : (
              <Navigate to="/dashboard" replace />
            )
          }
        />

        {/* Rutas protegidas */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          {/* Dashboard principal */}
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          
          {/* Perfil de usuario */}
          <Route path="profile" element={<Profile />} />
          
          {/* Módulo de Finanzas */}
          <Route path="finance/*" element={<FinancePage />} />
          
          {/* Módulo de Comunicación */}
          <Route path="communication/*" element={<CommunicationPage />} />
          
          {/* Módulo de Reservas */}
          <Route path="reservations/*" element={<ReservationsPage />} />
          
          {/* Módulo de Seguridad */}
          <Route path="security/*" element={<SecurityPage />} />
          
          {/* Módulo de Mantenimiento */}
          <Route path="maintenance/*" element={<MaintenancePage />} />
        </Route>

        {/* Ruta 404 */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Box>
  );
}

export default App;