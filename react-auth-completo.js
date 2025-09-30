// CÓDIGO REACT PARA TU CONFIGURACIÓN ESPECÍFICA
// Frontend: http://localhost:3000
// Backend: https://back-smart-condominium-1.onrender.com

import React, { useState, createContext, useContext, useEffect } from 'react';

// Configuración de la API
const API_BASE_URL = 'https://back-smart-condominium-1.onrender.com/api';

// Context para el usuario
const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de AuthProvider');
  }
  return context;
};

// Provider de autenticación
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Verificar si hay token al cargar
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/profile/`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
          setIsAuthenticated(true);
        } else {
          // Token inválido
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      } catch (error) {
        console.error('Error verificando autenticación:', error);
      }
    }
    setLoading(false);
  };

  // FUNCIÓN DE LOGIN (JWT ESTÁNDAR) - OPCIÓN RECOMENDADA
  const loginJWT = async (email, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          username: email,  // ⚠️ IMPORTANTE: 'username', no 'email'
          password: password
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Guardar tokens
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        
        // Obtener datos del usuario
        await checkAuthStatus();
        
        return { 
          success: true, 
          message: 'Login exitoso',
          tokens: data 
        };
      } else {
        return { 
          success: false, 
          message: data.detail || 'Credenciales inválidas',
          errors: data 
        };
      }
    } catch (error) {
      return { 
        success: false, 
        message: 'Error de conexión con el servidor',
        error: error.message 
      };
    }
  };

  // FUNCIÓN DE LOGIN (PERSONALIZADA) - OPCIÓN ALTERNATIVA
  const loginPersonalizado = async (email, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/iniciar-sesion/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          email: email,     // ✅ Aquí SÍ usa 'email'
          password: password
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Guardar tokens
        localStorage.setItem('access_token', data.tokens.access);
        localStorage.setItem('refresh_token', data.tokens.refresh);
        
        // Establecer usuario directamente (viene en la respuesta)
        setUser(data.usuario);
        setIsAuthenticated(true);
        
        return { 
          success: true, 
          message: data.mensaje,
          user: data.usuario,
          tokens: data.tokens 
        };
      } else {
        return { 
          success: false, 
          message: 'Credenciales inválidas',
          errors: data 
        };
      }
    } catch (error) {
      return { 
        success: false, 
        message: 'Error de conexión con el servidor',
        error: error.message 
      };
    }
  };

  // FUNCIÓN DE LOGOUT
  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (refreshToken) {
        await fetch(`${API_BASE_URL}/auth/logout/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: JSON.stringify({
            refresh: refreshToken
          })
        });
      }
    } catch (error) {
      console.error('Error en logout:', error);
    } finally {
      // Limpiar storage y estado
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  // FUNCIÓN PARA RENOVAR TOKEN
  const refreshAccessToken = async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
      logout();
      return false;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh: refreshToken
        })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        return true;
      } else {
        logout();
        return false;
      }
    } catch (error) {
      console.error('Error renovando token:', error);
      logout();
      return false;
    }
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    loginJWT,
    loginPersonalizado,
    logout,
    refreshAccessToken,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// COMPONENTE DE LOGIN
export const LoginForm = () => {
  const { loginJWT, loginPersonalizado } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [usePersonalizado, setUsePersonalizado] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Elegir método de login
    const loginMethod = usePersonalizado ? loginPersonalizado : loginJWT;
    const result = await loginMethod(formData.email, formData.password);

    if (result.success) {
      console.log('Login exitoso:', result);
      // Aquí puedes redirigir o actualizar el estado de la app
      // Por ejemplo: history.push('/dashboard') o window.location.href = '/dashboard'
    } else {
      setError(result.message);
      console.error('Error de login:', result);
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
      <h2>Iniciar Sesión</h2>
      
      {/* Toggle para elegir método de login */}
      <div style={{ marginBottom: '20px' }}>
        <label>
          <input
            type="checkbox"
            checked={usePersonalizado}
            onChange={(e) => setUsePersonalizado(e.target.checked)}
          />
          {' '}Usar endpoint personalizado
        </label>
        <small style={{ display: 'block', color: '#666' }}>
          {usePersonalizado ? 'Usando /auth/iniciar-sesion/' : 'Usando /auth/login/ (JWT estándar)'}
        </small>
      </div>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            style={{ 
              width: '100%', 
              padding: '8px', 
              marginTop: '5px',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            style={{ 
              width: '100%', 
              padding: '8px', 
              marginTop: '5px',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}
          />
        </div>

        {error && (
          <div style={{ 
            color: 'red', 
            marginBottom: '15px',
            padding: '10px',
            backgroundColor: '#ffe6e6',
            border: '1px solid #ff9999',
            borderRadius: '4px'
          }}>
            {error}
          </div>
        )}

        <button 
          type="submit" 
          disabled={loading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
        </button>
      </form>
    </div>
  );
};

// HOOK PARA PETICIONES AUTENTICADAS
export const useApiRequest = () => {
  const { refreshAccessToken, logout } = useAuth();

  const apiRequest = async (url, options = {}) => {
    const token = localStorage.getItem('access_token');
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
      }
    };

    let response = await fetch(url, { ...options, ...defaultOptions });

    // Si el token expiró, intentar renovarlo
    if (response.status === 401) {
      const refreshed = await refreshAccessToken();
      
      if (refreshed) {
        // Reintentar con el nuevo token
        const newToken = localStorage.getItem('access_token');
        defaultOptions.headers.Authorization = `Bearer ${newToken}`;
        response = await fetch(url, { ...options, ...defaultOptions });
      } else {
        // No se pudo renovar, logout
        logout();
        throw new Error('Sesión expirada');
      }
    }

    return response;
  };

  return { apiRequest };
};

// EJEMPLO DE USO EN APP.JS
/*
import { AuthProvider, LoginForm, useAuth } from './auth';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <MainContent />
      </div>
    </AuthProvider>
  );
}

function MainContent() {
  const { isAuthenticated, loading, user, logout } = useAuth();

  if (loading) {
    return <div>Cargando...</div>;
  }

  if (!isAuthenticated) {
    return <LoginForm />;
  }

  return (
    <div>
      <h1>Bienvenido, {user?.nombre_completo || user?.email}</h1>
      <button onClick={logout}>Cerrar Sesión</button>
      {/* Tu contenido principal aquí *\/}
    </div>
  );
}
*/