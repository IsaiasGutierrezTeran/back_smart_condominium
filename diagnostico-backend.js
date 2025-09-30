// Diagnóstico para verificar formato de credenciales del backend Django
// Copia y pega este código en la consola del navegador (F12)

console.log('🚀 INICIANDO DIAGNÓSTICO DEL BACKEND...\n');

// Configuración - REEMPLAZA con la URL de tu backend desplegado
const BACKEND_URL = 'https://tu-backend-desplegado.com'; // ⚠️ CAMBIAR ESTA URL
const API_BASE = `${BACKEND_URL}/api`;

// Credenciales de prueba - REEMPLAZA con credenciales válidas de tu sistema
const TEST_CREDENTIALS = {
    email: 'test@ejemplo.com',     // ⚠️ CAMBIAR POR EMAIL VÁLIDO
    password: 'password123'        // ⚠️ CAMBIAR POR PASSWORD VÁLIDO
};

console.log(`📍 URL del backend: ${BACKEND_URL}`);
console.log(`📧 Email de prueba: ${TEST_CREDENTIALS.email}`);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// Función para probar diferentes endpoints y formatos
async function probarEndpoints() {
    const endpoints = [
        // JWT estándar (SimpleJWT)
        {
            name: 'JWT Standard Login',
            url: `${API_BASE}/auth/login/`,
            method: 'POST',
            body: {
                username: TEST_CREDENTIALS.email,  // SimpleJWT usa 'username'
                password: TEST_CREDENTIALS.password
            }
        },
        
        // Endpoint personalizado
        {
            name: 'Custom Login (iniciar-sesion)',
            url: `${API_BASE}/auth/iniciar-sesion/`,
            method: 'POST',
            body: {
                email: TEST_CREDENTIALS.email,
                password: TEST_CREDENTIALS.password
            }
        },
        
        // Variante con email como username
        {
            name: 'JWT con email como username',
            url: `${API_BASE}/auth/login/`,
            method: 'POST',
            body: {
                email: TEST_CREDENTIALS.email,
                password: TEST_CREDENTIALS.password
            }
        }
    ];

    for (const endpoint of endpoints) {
        console.log(`🔍 PROBANDO: ${endpoint.name}`);
        console.log(`📡 URL: ${endpoint.url}`);
        console.log(`📋 Datos enviados:`, endpoint.body);
        
        try {
            const response = await fetch(endpoint.url, {
                method: endpoint.method,
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify(endpoint.body)
            });

            console.log(`📊 Status: ${response.status} ${response.statusText}`);
            
            const contentType = response.headers.get('content-type');
            console.log(`📄 Content-Type: ${contentType}`);

            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                console.log(`✅ Respuesta JSON:`, data);
                
                // Verificar si tiene tokens JWT
                if (data.access || data.tokens) {
                    console.log('🎉 ¡LOGIN EXITOSO! - Este endpoint funciona');
                    console.log('📝 Formato correcto de credenciales:', endpoint.body);
                }
            } else {
                const text = await response.text();
                console.log(`📄 Respuesta texto:`, text);
            }
            
        } catch (error) {
            console.log(`❌ Error de conexión:`, error.message);
            
            if (error.message.includes('CORS')) {
                console.log('🚨 PROBLEMA DE CORS detectado');
            }
            if (error.message.includes('Failed to fetch')) {
                console.log('🚨 No se puede conectar al servidor - verificar URL');
            }
        }
        
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    }
}

// Función para verificar CORS
async function verificarCORS() {
    console.log('🌐 VERIFICANDO CONFIGURACIÓN CORS...\n');
    
    try {
        const response = await fetch(`${API_BASE}/auth/login/`, {
            method: 'OPTIONS',
            headers: {
                'Origin': window.location.origin,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        });
        
        console.log(`📊 CORS Status: ${response.status}`);
        console.log('📋 Headers CORS:');
        
        response.headers.forEach((value, key) => {
            if (key.toLowerCase().includes('access-control')) {
                console.log(`   ${key}: ${value}`);
            }
        });
        
    } catch (error) {
        console.log(`❌ Error verificando CORS:`, error.message);
    }
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
}

// Función principal
async function ejecutarDiagnostico() {
    // Verificar si las URLs están configuradas
    if (BACKEND_URL === 'https://tu-backend-desplegado.com') {
        console.log('⚠️  IMPORTANTE: Debes cambiar BACKEND_URL por la URL real de tu backend');
        console.log('⚠️  IMPORTANTE: Debes cambiar TEST_CREDENTIALS por credenciales válidas');
        console.log('⚠️  Edita este archivo y vuelve a ejecutarlo\n');
        return;
    }
    
    await verificarCORS();
    await probarEndpoints();
    
    console.log('📋 RESUMEN DEL DIAGNÓSTICO:');
    console.log('1. Si ves "LOGIN EXITOSO" - usa ese formato en React');
    console.log('2. Si ves errores CORS - configura CORS en Django');
    console.log('3. Si ves "Failed to fetch" - verifica la URL del backend');
    console.log('4. Si ves errores 401/400 - verifica las credenciales');
    console.log('\n🎯 PRÓXIMOS PASOS:');
    console.log('1. Abre http://localhost:3000 en tu navegador');
    console.log('2. Presiona F12 → Console');
    console.log('3. Copia y pega este código modificado');
    console.log('4. Comparte los resultados para resolver el problema');
}

// Ejecutar el diagnóstico
ejecutarDiagnostico();