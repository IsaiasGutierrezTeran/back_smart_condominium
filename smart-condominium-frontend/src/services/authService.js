// Smart Condominium - Servicio de Autenticación
import api, { setAuthTokens, clearAuthTokens, handleApiError } from './api';

class AuthService {
  // Iniciar sesión
  async login(username, password) {
    try {
      const response = await api.post('/api/auth/iniciar-sesion/', {
        username,
        password,
      });

      const { tokens, usuario } = response.data;
      
      // Guardar tokens
      setAuthTokens(tokens.access, tokens.refresh);
      
      return {
        success: true,
        user: usuario,
        tokens,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Registrar usuario
  async register(userData) {
    try {
      const response = await api.post('/api/auth/registrar/', userData);
      
      const { tokens, usuario } = response.data;
      
      // Guardar tokens
      setAuthTokens(tokens.access, tokens.refresh);
      
      return {
        success: true,
        user: usuario,
        tokens,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Cerrar sesión
  async logout() {
    try {
      await api.post('/api/auth/logout/');
    } catch (error) {
      console.error('Error during logout:', error);
    } finally {
      clearAuthTokens();
    }
  }

  // Obtener perfil del usuario
  async getProfile() {
    try {
      const response = await api.get('/api/auth/perfil/');
      return {
        success: true,
        user: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Actualizar perfil
  async updateProfile(profileData) {
    try {
      const response = await api.patch('/api/auth/perfil/', profileData);
      return {
        success: true,
        user: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Cambiar contraseña
  async changePassword(passwordData) {
    try {
      const response = await api.post('/api/auth/change-password/', passwordData);
      return {
        success: true,
        message: response.data.message || 'Contraseña actualizada exitosamente',
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Refrescar token
  async refreshToken() {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await api.post('/api/auth/token/refresh/', {
        refresh: refreshToken,
      });

      const { access } = response.data;
      localStorage.setItem('accessToken', access);
      
      return {
        success: true,
        token: access,
      };
    } catch (error) {
      clearAuthTokens();
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Verificar si hay sesión activa
  isAuthenticated() {
    const token = localStorage.getItem('accessToken');
    if (!token) return false;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const now = Date.now() / 1000;
      return payload.exp > now;
    } catch {
      return false;
    }
  }

  // Obtener usuario actual del token
  getCurrentUser() {
    const token = localStorage.getItem('accessToken');
    if (!token) return null;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return {
        id: payload.user_id,
        username: payload.username,
        email: payload.email,
        rol: payload.rol,
        exp: payload.exp,
      };
    } catch {
      return null;
    }
  }

  // Obtener rol del usuario
  getUserRole() {
    const user = this.getCurrentUser();
    return user?.rol || null;
  }

  // Verificar permisos
  hasPermission(requiredRole) {
    const userRole = this.getUserRole();
    if (!userRole) return false;

    // Jerarquía de roles
    const roleHierarchy = {
      administrador: 4,
      seguridad: 3,
      mantenimiento: 2,
      residente: 1,
    };

    const userLevel = roleHierarchy[userRole] || 0;
    const requiredLevel = roleHierarchy[requiredRole] || 0;

    return userLevel >= requiredLevel;
  }

  // Verificar si es administrador
  isAdmin() {
    return this.getUserRole() === 'administrador';
  }

  // Verificar si es residente
  isResident() {
    return this.getUserRole() === 'residente';
  }

  // Verificar si es personal de seguridad
  isSecurity() {
    return this.getUserRole() === 'seguridad';
  }

  // Verificar si es personal de mantenimiento
  isMaintenance() {
    return this.getUserRole() === 'mantenimiento';
  }

  // Solicitar restablecimiento de contraseña
  async requestPasswordReset(email) {
    try {
      const response = await api.post('/api/auth/password-reset/', { email });
      return {
        success: true,
        message: response.data.message || 'Se ha enviado un enlace de restablecimiento a su email',
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Confirmar restablecimiento de contraseña
  async confirmPasswordReset(token, newPassword) {
    try {
      const response = await api.post('/api/auth/password-reset-confirm/', {
        token,
        new_password: newPassword,
      });
      return {
        success: true,
        message: response.data.message || 'Contraseña restablecida exitosamente',
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener usuarios (solo para administradores)
  async getUsers(params = {}) {
    try {
      const response = await api.get('/api/auth/users/', { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Crear usuario (solo para administradores)
  async createUser(userData) {
    try {
      const response = await api.post('/api/auth/users/', userData);
      return {
        success: true,
        user: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Actualizar usuario (solo para administradores)
  async updateUser(userId, userData) {
    try {
      const response = await api.patch(`/api/auth/users/${userId}/`, userData);
      return {
        success: true,
        user: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Eliminar usuario (solo para administradores)
  async deleteUser(userId) {
    try {
      await api.delete(`/api/auth/users/${userId}/`);
      return {
        success: true,
        message: 'Usuario eliminado exitosamente',
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }
}

export default new AuthService();