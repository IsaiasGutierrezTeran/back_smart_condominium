// CÓDIGO REACT CORRECTO PARA TU BACKEND
// Copia este código en tu componente de login en React

const API_BASE_URL = 'https://back-smart-condominium-1.onrender.com/api';

// ✅ OPCIÓN 1: Usando JWT estándar (RECOMENDADO)
const loginJWT = async (email, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        username: email,  // ⚠️ IMPORTANTE: usar 'username', NO 'email'
        password: password
      })
    });

    const data = await response.json();
    
    if (response.ok) {
      // ✅ Login exitoso
      console.log('Login exitoso:', data);
      
      // Guardar tokens en localStorage
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      
      return { 
        success: true, 
        data: data,
        tokens: {
          access: data.access,
          refresh: data.refresh
        }
      };
    } else {
      // ❌ Error de credenciales
      console.error('Error de login:', data);
      return { 
        success: false, 
        error: data.detail || 'Credenciales inválidas' 
      };
    }
    
  } catch (error) {
    // ❌ Error de conexión
    console.error('Error de conexión:', error);
    return { 
      success: false, 
      error: 'No se pudo conectar al servidor' 
    };
  }
};

// ✅ OPCIÓN 2: Usando tu endpoint personalizado 
const loginCustom = async (email, password) => {
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
      // ✅ Login exitoso
      console.log('Login exitoso:', data);
      
      // Guardar tokens en localStorage
      localStorage.setItem('access_token', data.tokens.access);
      localStorage.setItem('refresh_token', data.tokens.refresh);
      
      return { 
        success: true, 
        data: data,
        user: data.usuario,
        tokens: data.tokens
      };
    } else {
      // ❌ Error de credenciales
      console.error('Error de login:', data);
      return { 
        success: false, 
        error: data.detail || 'Credenciales inválidas' 
      };
    }
    
  } catch (error) {
    // ❌ Error de conexión
    console.error('Error de conexión:', error);
    return { 
      success: false, 
      error: 'No se pudo conectar al servidor' 
    };
  }
};

// 🎯 EJEMPLO DE USO EN COMPONENTE REACT
const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // ✅ USA ESTA FUNCIÓN (la que funcione mejor)
    const result = await loginJWT(email, password);
    // O alternativamente: const result = await loginCustom(email, password);
    
    if (result.success) {
      // ✅ Redirigir al dashboard o actualizar estado
      console.log('Usuario logueado:', result.data);
      // history.push('/dashboard') o lo que uses para navegación
    } else {
      // ❌ Mostrar error
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
      </button>
      {error && <div style={{color: 'red'}}>{error}</div>}
    </form>
  );
};

// 🔐 FUNCIÓN PARA USAR TOKENS EN OTRAS PETICIONES
const makeAuthenticatedRequest = async (url, options = {}) => {
  const token = localStorage.getItem('access_token');
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers
    }
  };
  
  const response = await fetch(url, { ...options, ...defaultOptions });
  
  if (response.status === 401) {
    // Token expirado, intentar renovar
    const refreshed = await refreshToken();
    if (refreshed) {
      // Reintentar con nuevo token
      return makeAuthenticatedRequest(url, options);
    } else {
      // Redirigir al login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
  }
  
  return response;
};

// 🔄 FUNCIÓN PARA RENOVAR TOKEN
const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  
  if (!refreshToken) return false;
  
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
    }
  } catch (error) {
    console.error('Error renovando token:', error);
  }
  
  return false;
};

export { loginJWT, loginCustom, makeAuthenticatedRequest, refreshToken };