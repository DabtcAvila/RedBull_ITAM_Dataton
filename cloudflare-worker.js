// 🏠 CasaMX - Cloudflare Worker
// Sirve la aplicación CasaMX desde GitHub Raw
// Asigna este worker al dominio casamx.app

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)
    
    // Ruta de salud para verificar que funciona
    if (url.pathname === '/health') {
      return new Response('CasaMX Worker OK', {
        headers: { 'Content-Type': 'text/plain' }
      })
    }
    
    // URL del index.html en GitHub
    const githubUrl = 'https://raw.githubusercontent.com/DabtcAvila/RedBull_ITAM_Dataton/main/index.html'
    
    try {
      console.log('Fetching CasaMX from GitHub...')
      const response = await fetch(githubUrl, {
        cf: {
          // Cachear por 5 minutos en Cloudflare edge
          cacheTtl: 300,
          cacheEverything: true,
        }
      })
      
      if (!response.ok) {
        console.error('GitHub fetch failed:', response.status)
        return new Response(`
          <h1>🏠 CasaMX - Temporalmente no disponible</h1>
          <p>El servicio está siendo actualizado. Intenta en unos minutos.</p>
          <p>Error: ${response.status}</p>
          <hr>
          <small>Datatón ITAM 2025 - David Fernando Ávila Díaz</small>
        `, { 
          status: 503,
          headers: { 'Content-Type': 'text/html;charset=UTF-8' }
        })
      }
      
      const html = await response.text()
      console.log('CasaMX loaded successfully')
      
      return new Response(html, {
        headers: {
          'Content-Type': 'text/html;charset=UTF-8',
          'Cache-Control': 'public, max-age=300',
          'Access-Control-Allow-Origin': '*',
          'X-Powered-By': 'CasaMX-Cloudflare-Worker',
          'X-GitHub-Source': 'DabtcAvila/RedBull_ITAM_Dataton'
        }
      })
      
    } catch (error) {
      console.error('Worker error:', error)
      return new Response(`
        <h1>🏠 CasaMX</h1>
        <h2>Servicio temporalmente no disponible</h2>
        <p>Estamos trabajando para restaurar el servicio.</p>
        <p><strong>Error:</strong> ${error.message}</p>
        <hr>
        <p><strong>Datatón ITAM 2025</strong><br>
        David Fernando Ávila Díaz</p>
        <p>🔄 <a href="javascript:location.reload()">Reintentar</a></p>
      `, { 
        status: 503,
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      })
    }
  }
}