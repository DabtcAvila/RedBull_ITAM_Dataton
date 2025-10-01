export default {
  async fetch(request) {
    return new Response(`
      <!DOCTYPE html>
      <html lang="es">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CasaMX - Tu hogar ideal en México</title>
        <style>
          body {
            font-family: system-ui;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            min-height: 100vh;
            margin: 0;
          }
          .container { max-width: 800px; margin: 0 auto; }
          h1 { font-size: 4rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
          .demo { background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px; margin: 2rem 0; }
          button { background: #4ECDC4; border: none; padding: 1rem 2rem; border-radius: 10px; color: white; font-weight: bold; cursor: pointer; font-size: 1.1rem; }
          button:hover { background: #45b7aa; transform: translateY(-2px); }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🏠 CasaMX</h1>
          <h2>Tu hogar ideal en México</h2>
          <p style="font-size: 1.2rem; margin-bottom: 2rem;">Recomendaciones personalizadas de zonas en CDMX para extranjeros</p>
          
          <div class="demo">
            <h3>🎯 Demo Funcionando</h3>
            <p><strong>Top 3 Zonas Recomendadas:</strong></p>
            <div style="text-align: left; max-width: 400px; margin: 0 auto;">
              <p>🏆 <strong>1. Polanco</strong> - Seguridad 95/100 - $45,000/mes</p>
              <p>🥈 <strong>2. Roma Norte</strong> - Seguridad 85/100 - $25,000/mes</p>
              <p>🥉 <strong>3. Condesa</strong> - Seguridad 82/100 - $28,000/mes</p>
            </div>
            <button onclick="alert('✅ CasaMX Worker funcionando perfectamente!')">Probar Demo</button>
          </div>
          
          <div style="margin-top: 3rem; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 2rem;">
            <h3>🏆 Datatón ITAM 2025</h3>
            <p><strong>David Fernando Ávila Díaz</strong></p>
            <p>Instituto Tecnológico Autónomo de México</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">✅ Cloudflare Worker deployado exitosamente</p>
          </div>
        </div>
      </body>
      </html>
    `, {
      headers: {
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'public, max-age=300'
      }
    })
  }
}