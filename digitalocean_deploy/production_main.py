#!/usr/bin/env python3
"""
CasaMX Production FastAPI Application
Optimized for DigitalOcean deployment
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import sqlite3
import redis
from pathlib import Path
import os
import logging
from typing import Dict, List, Any
from pydantic import BaseModel
import time
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
import structlog

# Configuration
DATABASE_PATH = Path("data/casamx.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-me")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "casamx.store,www.casamx.store,localhost").split(",")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Setup structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = Counter('casamx_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('casamx_request_duration_seconds', 'Request duration')
DATABASE_QUERIES = Counter('casamx_database_queries_total', 'Database queries')
CACHE_HITS = Counter('casamx_cache_hits_total', 'Cache hits')
CACHE_MISSES = Counter('casamx_cache_misses_total', 'Cache misses')

# Redis connection
try:
    redis_client = redis.Redis.from_url(REDIS_URL, password=REDIS_PASSWORD, decode_responses=True)
    redis_client.ping()
    logger.info("Redis connection established")
except Exception as e:
    logger.error("Redis connection failed", error=str(e))
    redis_client = None

# Pydantic models
class ColoniaResponse(BaseModel):
    id: int
    nombre: str
    delegacion: str
    cp: str
    lat: float = None
    lng: float = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    database: str
    redis: str

# FastAPI app
app = FastAPI(
    title="CasaMX API",
    description="Sistema de Recomendaciones de Vivienda CDMX",
    version="1.0.0",
    docs_url="/api/docs" if DEBUG else None,
    redoc_url="/api/redoc" if DEBUG else None,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"https://{host}" for host in ALLOWED_HOSTS] + (["http://localhost:3000"] if DEBUG else []),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Static files (for production)
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Database helper
def get_db():
    """Get database connection"""
    if not DATABASE_PATH.exists():
        raise HTTPException(status_code=500, detail="Database not found")
    
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Cache helper
def get_from_cache(key: str) -> Any:
    """Get data from Redis cache"""
    if not redis_client:
        return None
    
    try:
        data = redis_client.get(key)
        if data:
            CACHE_HITS.inc()
            return data
        else:
            CACHE_MISSES.inc()
            return None
    except Exception as e:
        logger.error("Cache get failed", key=key, error=str(e))
        return None

def set_to_cache(key: str, value: str, ttl: int = 3600) -> bool:
    """Set data to Redis cache"""
    if not redis_client:
        return False
    
    try:
        redis_client.setex(key, ttl, value)
        return True
    except Exception as e:
        logger.error("Cache set failed", key=key, error=str(e))
        return False

# Middleware for metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Record metrics
    process_time = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(process_time)
    
    # Add performance headers
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Routes
@app.get("/")
async def root():
    """Root endpoint - serves frontend or API info"""
    if Path("static/index.html").exists():
        with open("static/index.html") as f:
            return HTMLResponse(f.read())
    
    return JSONResponse({
        "message": "CasaMX API",
        "status": "OK",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "api": "/api/",
            "colonias": "/api/colonias",
            "docs": "/api/docs" if DEBUG else "disabled"
        }
    })

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    
    # Check database
    db_status = "ok"
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        conn.execute("SELECT 1")
        conn.close()
        DATABASE_QUERIES.inc()
    except Exception as e:
        db_status = f"error: {str(e)}"
        logger.error("Database health check failed", error=str(e))
    
    # Check Redis
    redis_status = "ok"
    if redis_client:
        try:
            redis_client.ping()
        except Exception as e:
            redis_status = f"error: {str(e)}"
            logger.error("Redis health check failed", error=str(e))
    else:
        redis_status = "not configured"
    
    status = "healthy" if db_status == "ok" else "unhealthy"
    
    return HealthResponse(
        status=status,
        timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
        version="1.0.0",
        database=db_status,
        redis=redis_status
    )

@app.get("/api/")
async def api_root():
    """API root endpoint"""
    return JSONResponse({
        "message": "CasaMX API funcionando",
        "status": "OK",
        "version": "1.0.0",
        "environment": "production"
    })

@app.get("/api/colonias", response_model=List[ColoniaResponse])
async def get_colonias(
    limit: int = 50,
    offset: int = 0,
    delegacion: str = None,
    db=Depends(get_db)
):
    """Get colonias with optional filtering"""
    
    # Try cache first
    cache_key = f"colonias:{limit}:{offset}:{delegacion or 'all'}"
    cached_data = get_from_cache(cache_key)
    
    if cached_data:
        import json
        return json.loads(cached_data)
    
    try:
        cursor = db.cursor()
        
        # Build query
        query = "SELECT * FROM colonias"
        params = []
        
        if delegacion:
            query += " WHERE delegacion = ?"
            params.append(delegacion)
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        DATABASE_QUERIES.inc()
        
        # Convert to response model
        colonias = []
        for row in rows:
            colonia = ColoniaResponse(
                id=row.get('id', 0),
                nombre=row.get('nombre', ''),
                delegacion=row.get('delegacion', ''),
                cp=row.get('cp', ''),
                lat=row.get('lat'),
                lng=row.get('lng')
            )
            colonias.append(colonia)
        
        # Cache result
        import json
        cache_data = json.dumps([c.dict() for c in colonias])
        set_to_cache(cache_key, cache_data, ttl=1800)  # 30 minutes
        
        logger.info("Colonias fetched", count=len(colonias), delegacion=delegacion)
        
        return colonias
        
    except Exception as e:
        logger.error("Database query failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/delegaciones")
async def get_delegaciones(db=Depends(get_db)):
    """Get list of available delegaciones"""
    
    cache_key = "delegaciones:all"
    cached_data = get_from_cache(cache_key)
    
    if cached_data:
        import json
        return json.loads(cached_data)
    
    try:
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT delegacion FROM colonias ORDER BY delegacion")
        rows = cursor.fetchall()
        
        DATABASE_QUERIES.inc()
        
        delegaciones = [row[0] for row in rows if row[0]]
        
        # Cache result
        import json
        cache_data = json.dumps({"delegaciones": delegaciones})
        set_to_cache(cache_key, cache_data, ttl=3600)  # 1 hour
        
        return {"delegaciones": delegaciones}
        
    except Exception as e:
        logger.error("Database query failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/stats")
async def get_stats(db=Depends(get_db)):
    """Get basic statistics"""
    
    cache_key = "stats:general"
    cached_data = get_from_cache(cache_key)
    
    if cached_data:
        import json
        return json.loads(cached_data)
    
    try:
        cursor = db.cursor()
        
        # Get total colonias
        cursor.execute("SELECT COUNT(*) FROM colonias")
        total_colonias = cursor.fetchone()[0]
        
        # Get delegaciones count
        cursor.execute("SELECT COUNT(DISTINCT delegacion) FROM colonias")
        total_delegaciones = cursor.fetchone()[0]
        
        DATABASE_QUERIES.inc(2)
        
        stats = {
            "total_colonias": total_colonias,
            "total_delegaciones": total_delegaciones,
            "api_version": "1.0.0",
            "status": "active"
        }
        
        # Cache result
        import json
        cache_data = json.dumps(stats)
        set_to_cache(cache_key, cache_data, ttl=3600)  # 1 hour
        
        return stats
        
    except Exception as e:
        logger.error("Stats query failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type="text/plain")

@app.get("/api/search")
async def search_colonias(
    q: str,
    limit: int = 20,
    db=Depends(get_db)
):
    """Search colonias by name"""
    
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    cache_key = f"search:{q}:{limit}"
    cached_data = get_from_cache(cache_key)
    
    if cached_data:
        import json
        return json.loads(cached_data)
    
    try:
        cursor = db.cursor()
        
        # Search in nombre and delegacion
        query = """
        SELECT * FROM colonias 
        WHERE nombre LIKE ? OR delegacion LIKE ?
        LIMIT ?
        """
        search_term = f"%{q}%"
        cursor.execute(query, [search_term, search_term, limit])
        rows = cursor.fetchall()
        
        DATABASE_QUERIES.inc()
        
        results = []
        for row in rows:
            result = {
                "id": row.get('id', 0),
                "nombre": row.get('nombre', ''),
                "delegacion": row.get('delegacion', ''),
                "cp": row.get('cp', ''),
                "match_type": "nombre" if q.lower() in row.get('nombre', '').lower() else "delegacion"
            }
            results.append(result)
        
        response_data = {
            "query": q,
            "results": results,
            "total": len(results)
        }
        
        # Cache result
        import json
        cache_data = json.dumps(response_data)
        set_to_cache(cache_key, cache_data, ttl=1800)  # 30 minutes
        
        logger.info("Search performed", query=q, results=len(results))
        
        return response_data
        
    except Exception as e:
        logger.error("Search query failed", query=q, error=str(e))
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error("Internal server error", path=str(request.url.path), error=str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An internal error occurred"
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("CasaMX API starting up", version="1.0.0", debug=DEBUG)
    
    # Verify database exists
    if not DATABASE_PATH.exists():
        logger.error("Database file not found", path=str(DATABASE_PATH))
    else:
        logger.info("Database found", path=str(DATABASE_PATH))
    
    # Test Redis connection
    if redis_client:
        try:
            redis_client.ping()
            logger.info("Redis connection verified")
        except Exception as e:
            logger.error("Redis connection failed", error=str(e))

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("CasaMX API shutting down")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting CasaMX API on {host}:{port}")
    print(f"📖 Environment: {'development' if DEBUG else 'production'}")
    print(f"🗄️  Database: {DATABASE_PATH}")
    print(f"📊 Redis: {'enabled' if redis_client else 'disabled'}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info" if not DEBUG else "debug",
        access_log=True
    )