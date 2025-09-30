// PRUEBA ESPECÍFICA PARA TU CONFIGURACIÓN
// Frontend: http://localhost:3000
// Backend: https://back-smart-condominium-1.onrender.com

// ⚠️ CAMBIAR ESTAS CREDENCIALES POR UNAS VÁLIDAS DE TU SISTEMA
const TEST_EMAIL = 'test@ejemplo.com';      // ⚠️ CAMBIAR
const TEST_PASSWORD = 'password123';        // ⚠️ CAMBIAR

const API_URL = 'https://back-smart-condominium-1.onrender.com/api';

console.log('🚀 PROBANDO LOGIN DESDE LOCALHOST:3000');
console.log(`📧 Email: ${TEST_EMAIL}`);
console.log(`🔗 Backend: ${API_URL}`);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// PRUEBA 1: JWT Estándar (RECOMENDADO)
const pruebaJWT = async () => {
  console.log('🧪 PRUEBA 1: JWT Estándar (/api/auth/login/)');
  
  try {
    const response = await fetch(`${API_URL}/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        username: TEST_EMAIL,  // ⚠️ IMPORTANTE: 'username' no 'email'
        password: TEST_PASSWORD
      })
    });

    const data = await response.json();
    
    console.log(`📊 Status: ${response.status} ${response.statusText}`);
    console.log('📋 Headers importantes:');
    console.log(`   Content-Type: ${response.headers.get('content-type')}`);
    console.log(`   Access-Control-Allow-Origin: ${response.headers.get('access-control-allow-origin')}`);
    
    if (response.ok) {
      console.log('✅ ¡LOGIN JWT EXITOSO!');
      console.log('🔑 Access Token (primeros 50 chars):', data.access?.substring(0, 50) + '...');
      console.log('🔄 Refresh Token (primeros 50 chars):', data.refresh?.substring(0, 50) + '...');
      
      // Guardar tokens
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      
      console.log('💾 Tokens guardados en localStorage');
      return { success: true, method: 'JWT', tokens: data };
    } else {
      console.log('❌ Error JWT:', data);
      return { success: false, method: 'JWT', error: data };
    }
    
  } catch (error) {
    console.log('💥 Error de conexión JWT:', error.message);
    if (error.message.includes('CORS')) {
      console.log('🚨 PROBLEMA DE CORS detectado en JWT');
    }
    return { success: false, method: 'JWT', error: error.message };
  }
};

// PRUEBA 2: Endpoint Personalizado
const pruebaPersonalizado = async () => {
  console.log('\n🧪 PRUEBA 2: Endpoint Personalizado (/api/auth/iniciar-sesion/)');
  
  try {
    const response = await fetch(`${API_URL}/auth/iniciar-sesion/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        email: TEST_EMAIL,     // ✅ Aquí SÍ usa 'email'
        password: TEST_PASSWORD
      })
    });

    const data = await response.json();
    
    console.log(`📊 Status: ${response.status} ${response.statusText}`);
    
    if (response.ok) {
      console.log('✅ ¡LOGIN PERSONALIZADO EXITOSO!');
      console.log('👤 Usuario:', data.usuario);
      console.log('🔑 Access Token (primeros 50 chars):', data.tokens?.access?.substring(0, 50) + '...');
      console.log('🔄 Refresh Token (primeros 50 chars):', data.tokens?.refresh?.substring(0, 50) + '...');
      
      // Guardar tokens
      localStorage.setItem('access_token', data.tokens.access);
      localStorage.setItem('refresh_token', data.tokens.refresh);
      
      console.log('💾 Tokens guardados en localStorage');
      return { success: true, method: 'PERSONALIZADO', tokens: data.tokens, user: data.usuario };
    } else {
      console.log('❌ Error Personalizado:', data);
      return { success: false, method: 'PERSONALIZADO', error: data };
    }
    
  } catch (error) {
    console.log('💥 Error de conexión Personalizado:', error.message);
    return { success: false, method: 'PERSONALIZADO', error: error.message };
  }
};

// PRUEBA 3: Verificar que el token funciona
const probarToken = async (token) => {
  console.log('\n🧪 PRUEBA 3: Verificar que el token funciona');
  
  try {
    const response = await fetch(`${API_URL}/auth/profile/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      }
    });

    const data = await response.json();
    
    console.log(`📊 Status: ${response.status} ${response.statusText}`);
    
    if (response.ok) {
      console.log('✅ ¡TOKEN VÁLIDO!');
      console.log('👤 Perfil del usuario:', data);
      return { success: true, profile: data };
    } else {
      console.log('❌ Token inválido o expirado:', data);
      return { success: false, error: data };
    }
    
  } catch (error) {
    console.log('💥 Error verificando token:', error.message);
    return { success: false, error: error.message };
  }
};

// EJECUTAR TODAS LAS PRUEBAS
const ejecutarPruebas = async () => {
  // Verificar que las credenciales fueron cambiadas
  if (TEST_EMAIL === 'test@ejemplo.com' || TEST_PASSWORD === 'password123') {
    console.log('⚠️  IMPORTANTE: Debes cambiar TEST_EMAIL y TEST_PASSWORD por credenciales válidas');
    console.log('⚠️  Edita este archivo y vuelve a ejecutarlo');
    return;
  }
  
  console.log('🏁 INICIANDO TODAS LAS PRUEBAS...\n');
  
  // Probar JWT
  const resultadoJWT = await pruebaJWT();
  
  // Probar personalizado
  const resultadoPersonalizado = await pruebaPersonalizado();
  
  // Probar token si alguno funcionó
  let tokenParaProbar = null;
  if (resultadoJWT.success) {
    tokenParaProbar = resultadoJWT.tokens.access;
  } else if (resultadoPersonalizado.success) {
    tokenParaProbar = resultadoPersonalizado.tokens.access;
  }
  
  if (tokenParaProbar) {
    await probarToken(tokenParaProbar);
  }
  
  // RESUMEN FINAL
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📋 RESUMEN DE RESULTADOS:');
  console.log(`   JWT Estándar: ${resultadoJWT.success ? '✅ FUNCIONA' : '❌ NO FUNCIONA'}`);
  console.log(`   Personalizado: ${resultadoPersonalizado.success ? '✅ FUNCIONA' : '❌ NO FUNCIONA'}`);
  
  if (resultadoJWT.success || resultadoPersonalizado.success) {
    console.log('\n🎉 ¡AL MENOS UNO FUNCIONA!');
    console.log('💡 Usa el método que funciona en tu código React');
    console.log('📁 Revisa el archivo login-correcto.js para el código completo');
  } else {
    console.log('\n🔧 NINGUNO FUNCIONA - Posibles problemas:');
    console.log('   1. Credenciales incorrectas');
    console.log('   2. Usuario no existe en la base de datos');
    console.log('   3. Problema de CORS (aunque no debería)');
    console.log('   4. Backend no está funcionando correctamente');
  }
};

// EJECUTAR
ejecutarPruebas();