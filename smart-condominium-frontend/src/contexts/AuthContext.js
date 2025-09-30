// Smart Condominium - Context de Autenticación
import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import authService from '../services/authService';
import toast from 'react-hot-toast';

// Crear el contexto
const AuthContext = createContext();

// Hook para usar el contexto
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de AuthProvider');
  }
  return context;
};

// Estados del reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      };
    
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        isAuthenticated: true,
        loading: false,
        error: null,
      };
    
    case 'LOGIN_ERROR':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        loading: false,
        error: action.payload,
      };
    
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        loading: false,
        error: null,
      };
    
    case 'UPDATE_USER':
      return {
        ...state,
        user: { ...state.user, ...action.payload },
      };
    
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    
    default:
      return state;
  }
};

// Estado inicial
const initialState = {
  user: null,
  isAuthenticated: false,
  loading: true,
  error: null,
};

// Provider del contexto
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Verificar autenticación al cargar la aplicación
  useEffect(() => {
    checkAuthStatus();
  }, []);

  // Verificar estado de autenticación
  const checkAuthStatus = async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    
    try {
      const token = localStorage.getItem('accessToken');
      
      if (!token) {
        dispatch({ type: 'LOGOUT' });
        return;
      }

      // Verificar si el token es válido
      const decoded = jwtDecode(token);
      const now = Date.now() / 1000;
      
      if (decoded.exp <= now) {
        // Token expirado, intentar refrescar
        const refreshResult = await authService.refreshToken();
        if (!refreshResult.success) {
          dispatch({ type: 'LOGOUT' });
          return;
        }
      }

      // Obtener perfil del usuario
      const profileResult = await authService.getProfile();
      if (profileResult.success) {
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: { user: profileResult.user },
        });
      } else {
        dispatch({ type: 'LOGOUT' });
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
      dispatch({ type: 'LOGOUT' });
    }
  };

  // Iniciar sesión
  const login = async (username, password) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    
    try {
      const result = await authService.login(username, password);
      
      if (result.success) {
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: { user: result.user },
        });
        toast.success('¡Bienvenido a Smart Condominium!');
        return { success: true };
      } else {
        dispatch({
          type: 'LOGIN_ERROR',
          payload: result.error,
        });
        toast.error(result.error);
        return { success: false, error: result.error };
      }
    } catch (error) {
      const errorMessage = 'Error de conexión. Intente nuevamente.';
      dispatch({
        type: 'LOGIN_ERROR',
        payload: errorMessage,
      });
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  // Registrar usuario
  const register = async (userData) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    
    try {
      const result = await authService.register(userData);
      
      if (result.success) {
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: { user: result.user },
        });
        toast.success('¡Registro exitoso! Bienvenido a Smart Condominium!');
        return { success: true };
      } else {
        dispatch({
          type: 'LOGIN_ERROR',
          payload: result.error,
        });
        toast.error(result.error);
        return { success: false, error: result.error };
      }
    } catch (error) {
      const errorMessage = 'Error de conexión. Intente nuevamente.';
      dispatch({
        type: 'LOGIN_ERROR',
        payload: errorMessage,
      });
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  // Cerrar sesión
  const logout = async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    
    try {
      await authService.logout();
      dispatch({ type: 'LOGOUT' });
      toast.success('Sesión cerrada exitosamente');
    } catch (error) {
      console.error('Error during logout:', error);
      dispatch({ type: 'LOGOUT' });
    }
  };

  // Actualizar perfil
  const updateProfile = async (profileData) => {
    try {
      const result = await authService.updateProfile(profileData);
      
      if (result.success) {
        dispatch({
          type: 'UPDATE_USER',
          payload: result.user,
        });
        toast.success('Perfil actualizado exitosamente');
        return { success: true };
      } else {
        toast.error(result.error);
        return { success: false, error: result.error };
      }
    } catch (error) {
      const errorMessage = 'Error al actualizar el perfil';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  // Cambiar contraseña
  const changePassword = async (passwordData) => {
    try {
      const result = await authService.changePassword(passwordData);
      
      if (result.success) {
        toast.success(result.message);
        return { success: true };
      } else {
        toast.error(result.error);
        return { success: false, error: result.error };
      }
    } catch (error) {
      const errorMessage = 'Error al cambiar la contraseña';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  // Solicitar restablecimiento de contraseña
  const requestPasswordReset = async (email) => {
    try {
      const result = await authService.requestPasswordReset(email);
      
      if (result.success) {
        toast.success(result.message);
        return { success: true };
      } else {
        toast.error(result.error);
        return { success: false, error: result.error };
      }
    } catch (error) {
      const errorMessage = 'Error al solicitar restablecimiento';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  // Limpiar error
  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  // Verificar permisos
  const hasPermission = (requiredRole) => {
    return authService.hasPermission(requiredRole);
  };

  // Verificar rol específico
  const isAdmin = () => authService.isAdmin();
  const isResident = () => authService.isResident();
  const isSecurity = () => authService.isSecurity();
  const isMaintenance = () => authService.isMaintenance();

  // Obtener rol del usuario
  const getUserRole = () => {
    return state.user?.rol || authService.getUserRole();
  };

  // Valor del contexto
  const contextValue = {
    ...state,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    requestPasswordReset,
    clearError,
    checkAuthStatus,
    hasPermission,
    isAdmin,
    isResident,
    isSecurity,
    isMaintenance,
    getUserRole,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;