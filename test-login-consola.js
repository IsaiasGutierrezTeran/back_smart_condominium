// PRUEBA RÁPIDA - Ejecutar en consola del navegador (F12)
// ⚠️ CAMBIAR email y password por credenciales válidas de tu sistema

const testLogin = async () => {
  const email = 'tu-email@ejemplo.com';  // ⚠️ CAMBIAR
  const password = 'tu-password';        // ⚠️ CAMBIAR
  
  console.log('🧪 PROBANDO LOGIN...');
  
  try {
    const response = await fetch('https://back-smart-condominium-1.onrender.com/api/auth/login/', {
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
    
    console.log('📊 Status:', response.status);
    console.log('📋 Respuesta:', data);
    
    if (response.ok) {
      console.log('✅ ¡LOGIN EXITOSO!');
      console.log('🔑 Access Token:', data.access);
      console.log('🔄 Refresh Token:', data.refresh);
      
      // Guardar tokens para pruebas
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      
      return true;
    } else {
      console.log('❌ Error:', data);
      return false;
    }
    
  } catch (error) {
    console.log('💥 Error de conexión:', error);
    return false;
  }
};

// Ejecutar la prueba
testLogin().then(success => {
  if (success) {
    console.log('🎉 El login funciona correctamente!');
    console.log('💡 Usa el código de login-correcto.js en tu React');
  } else {
    console.log('🔧 Revisa las credenciales o contacta al desarrollador');
  }
});