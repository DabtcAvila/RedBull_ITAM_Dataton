// 🏠 CasaMX - Modern Cloudflare Worker (2024/2025)
// Sirve la aplicación CasaMX desde GitHub Raw
// Sintaxis addEventListener compatible con todas las versiones

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // Health check endpoint
  if (url.pathname === '/health') {
    return new Response('CasaMX Worker OK - 2024', {
      headers: { 'Content-Type': 'text/plain' }
    })
  }
  
  // GitHub Raw URL para index.html
  const githubUrl = 'https://raw.githubusercontent.com/DabtcAvila/RedBull_ITAM_Dataton/main/index.html'
  
  try {
    const response = await fetch(githubUrl, {
      headers: {
        'User-Agent': 'CasaMX-Cloudflare-Worker-2024',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      }
    })
    
    if (!response.ok) {
      throw new Error(`GitHub fetch failed: ${response.status} ${response.statusText}`)
    }
    
    const html = await response.text()
    
    // Verificar que el HTML no está vacío
    if (!html || html.length < 100) {
      throw new Error('Empty or invalid HTML received')
    }
    
    return new Response(html, {
      headers: {
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'public, max-age=300',
        'Access-Control-Allow-Origin': '*',
        'X-Powered-By': 'CasaMX-Worker-2024',
        'X-GitHub-Source': 'DabtcAvila/RedBull_ITAM_Dataton'
      }
    })
    
  } catch (error) {
    return new Response(`
      <!DOCTYPE html>
      <html lang="es-MX">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CasaMX - Cargando...</title>
        <style>
          body { font-family: system-ui; text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
          .container { max-width: 600px; margin: 0 auto; }
          button { background: #4ECDC4; border: none; padding: 1rem 2rem; border-radius: 10px; color: white; font-weight: bold; cursor: pointer; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🏠 CasaMX</h1>
          <h2>Servicio Temporalmente No Disponible</h2>
          <p><strong>Error:</strong> ${error.message}</p>
          <p>Datatón ITAM 2025 - David Fernando Ávila Díaz</p>
          <button onclick="location.reload()">🔄 Reintentar</button>
        </div>
      </body>
      </html>
    `, { 
      status: 503,
      headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    })
  }
}