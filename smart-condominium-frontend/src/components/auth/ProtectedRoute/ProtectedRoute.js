// Smart Condominium - Ruta protegida
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../../contexts/AuthContext';
import LoadingSpinner from '../../common/LoadingSpinner/LoadingSpinner';

const ProtectedRoute = ({ children, requiredRole = null }) => {
  const { isAuthenticated, loading, hasPermission } = useAuth();
  const location = useLocation();

  // Mostrar spinner mientras se verifica la autenticación
  if (loading) {
    return <LoadingSpinner fullScreen message="Verificando acceso..." />;
  }

  // Si no está autenticado, redirigir al login
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Si se requiere un rol específico y el usuario no tiene permisos
  if (requiredRole && !hasPermission(requiredRole)) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

export default ProtectedRoute;