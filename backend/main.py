from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import sys
import asyncio

# Fix para Windows + Python 3.13 + Playwright
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from models import ContratacionResponse
from scraper import get_contrataciones  # Habilitado para probar con buscador público

# Cargar variables de entorno
load_dotenv(dotenv_path="../.env")

app = FastAPI(
    title="SEACE Scraper API",
    description="API para buscar contrataciones menores en SEACE",
    version="1.0.0"
)

# Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "SEACE Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "contrataciones": "/api/contrataciones",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/contrataciones", response_model=ContratacionResponse)
def obtener_contrataciones():
    """
    Obtiene las contrataciones de tecnología y bienes/servicios de Lima
    que están vigentes o próximas a publicarse
    """
    try:
        # Usar el scraper real con el buscador público (no requiere credenciales reales)
        username = os.getenv("user", "")
        password = os.getenv("pass", "")
        contrataciones = get_contrataciones(username, password)

        return ContratacionResponse(
            contrataciones=contrataciones,
            total=len(contrataciones),
            timestamp=datetime.now(timezone.utc)
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener contrataciones: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
