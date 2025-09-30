// Smart Condominium - Configuración API
import axios from 'axios';
import jwtDecode from 'jwt-decode';
import toast from 'react-hot-toast';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://back-smart-condominium-1.onrender.com';

// Crear instancia de axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 segundos
});

// Interceptor para agregar token de autorización
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejo de respuestas y refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Si el error es 401 y no es un retry
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/api/auth/token/refresh/`, {
            refresh: refreshToken
          });
          
          const { access } = response.data;
          localStorage.setItem('accessToken', access);
          
          // Reintentar la petición original
          return api(originalRequest);
        } catch (refreshError) {
          // Si el refresh falla, limpiar tokens y redirigir al login
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
          toast.error('Sesión expirada. Por favor, inicie sesión nuevamente.');
        }
      } else {
        // No hay refresh token, redirigir al login
        window.location.href = '/login';
        toast.error('Por favor, inicie sesión.');
      }
    }
    
    // Manejo de errores comunes
    if (error.response) {
      const { status } = error.response;
      
      switch (status) {
        case 403:
          toast.error('No tiene permisos para realizar esta acción.');
          break;
        case 404:
          toast.error('Recurso no encontrado.');
          break;
        case 500:
          toast.error('Error interno del servidor. Intente nuevamente.');
          break;
        case 503:
          toast.error('Servicio no disponible. Intente más tarde.');
          break;
        default:
          if (error.response.data?.detail) {
            toast.error(error.response.data.detail);
          } else if (error.response.data?.message) {
            toast.error(error.response.data.message);
          }
      }
    } else if (error.request) {
      toast.error('Error de conexión. Verifique su conexión a internet.');
    }
    
    return Promise.reject(error);
  }
);

// Funciones auxiliares para el manejo de tokens
export const setAuthTokens = (accessToken, refreshToken) => {
  localStorage.setItem('accessToken', accessToken);
  localStorage.setItem('refreshToken', refreshToken);
};

export const clearAuthTokens = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
};

export const getAccessToken = () => {
  return localStorage.getItem('accessToken');
};

export const getRefreshToken = () => {
  return localStorage.getItem('refreshToken');
};

export const isTokenValid = (token) => {
  if (!token) return false;
  
  try {
    const decoded = jwtDecode(token);
    const now = Date.now() / 1000;
    return decoded.exp > now;
  } catch {
    return false;
  }
};

export const getUserFromToken = (token) => {
  if (!token) return null;
  
  try {
    return jwtDecode(token);
  } catch {
    return null;
  }
};

// Funciones de utilidad para requests
export const handleApiError = (error) => {
  if (error.response?.data) {
    // Errores del servidor con datos
    const errorData = error.response.data;
    
    if (typeof errorData === 'string') {
      return errorData;
    }
    
    if (errorData.detail) {
      return errorData.detail;
    }
    
    if (errorData.message) {
      return errorData.message;
    }
    
    // Errores de validación de campos
    if (typeof errorData === 'object') {
      const errors = [];
      Object.keys(errorData).forEach(field => {
        const fieldErrors = Array.isArray(errorData[field]) 
          ? errorData[field] 
          : [errorData[field]];
        errors.push(...fieldErrors);
      });
      return errors.length > 0 ? errors.join(', ') : 'Error en los datos enviados';
    }
  }
  
  if (error.message) {
    return error.message;
  }
  
  return 'Ha ocurrido un error inesperado';
};

// Configuraciones para diferentes tipos de contenido
export const apiConfig = {
  json: {
    headers: {
      'Content-Type': 'application/json',
    },
  },
  
  formData: {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  },
  
  download: {
    responseType: 'blob',
  },
};

// Funciones para crear requests comunes
export const createGetRequest = (url, params = {}) => {
  return api.get(url, { params });
};

export const createPostRequest = (url, data, config = {}) => {
  return api.post(url, data, config);
};

export const createPutRequest = (url, data, config = {}) => {
  return api.put(url, data, config);
};

export const createPatchRequest = (url, data, config = {}) => {
  return api.patch(url, data, config);
};

export const createDeleteRequest = (url, config = {}) => {
  return api.delete(url, config);
};

// Helper para manejar paginación
export const createPaginatedRequest = (url, page = 1, pageSize = 10, filters = {}) => {
  const params = {
    page,
    page_size: pageSize,
    ...filters,
  };
  
  return api.get(url, { params });
};

// Helper para subir archivos
export const uploadFile = (url, file, onProgress = null) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const config = {
    ...apiConfig.formData,
    onUploadProgress: onProgress ? (progressEvent) => {
      const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      onProgress(percentCompleted);
    } : undefined,
  };
  
  return api.post(url, formData, config);
};

// Helper para descargar archivos
export const downloadFile = async (url, filename) => {
  try {
    const response = await api.get(url, apiConfig.download);
    
    // Crear un blob del archivo
    const blob = new Blob([response.data]);
    const downloadUrl = window.URL.createObjectURL(blob);
    
    // Crear elemento de descarga
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    
    // Limpiar
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
  } catch (error) {
    toast.error('Error al descargar el archivo');
    throw error;
  }
};

export default api;