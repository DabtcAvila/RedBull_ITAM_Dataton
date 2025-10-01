// Cloudflare Worker para servir CasaMX desde GitHub
// Asigna este worker a casamx.app en Cloudflare

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // Redirigir todas las requests al index.html de GitHub
  const githubUrl = 'https://raw.githubusercontent.com/DabtcAvila/RedBull_ITAM_Dataton/main/index.html'
  
  try {
    const response = await fetch(githubUrl)
    
    if (!response.ok) {
      return new Response('Error loading CasaMX', { status: 404 })
    }
    
    const html = await response.text()
    
    return new Response(html, {
      headers: {
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'public, max-age=300', // Cache 5 minutes
        'Access-Control-Allow-Origin': '*',
      },
    })
  } catch (error) {
    return new Response('CasaMX temporalmente no disponible', { 
      status: 503,
      headers: {
        'Content-Type': 'text/html;charset=UTF-8'
      }
    })
  }
}