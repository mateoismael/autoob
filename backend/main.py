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
# from scraper import get_contrataciones  # Comentado temporalmente por issue con Playwright en Windows

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
        # TEMPORAL: Datos de muestra mientras resolvemos el issue de Playwright en Windows
        from datetime import timedelta
        from models import Contratacion

        contrataciones_muestra = [
            Contratacion(
                codigo="CM-117-2025-CPMP",
                descripcion="SERVICIO DE RENOVACIÓN E INSTALACIÓN DE ALFOMBRAS DEL DPTO. DE ATENCIÓN AL AFILIADO Y DPTO. DE GESTIÓN DE BENEFICIOS PREVISIONALES",
                entidad="CAJA DE PENSIONES MILITAR - POLICIAL",
                fecha_limite=datetime.now(timezone.utc) + timedelta(hours=18),
                tiempo_restante_horas=18.0,
                estado_tiempo="rojo",
                url_detalle="https://prod6.seace.gob.pe/buscador-publico/contrataciones/30529",
                fecha_publicacion=datetime.now(timezone.utc) - timedelta(days=1)
            ),
            Contratacion(
                codigo="CM-101-2025-INICTEL-UNI",
                descripcion="Servicio de asistencia técnica para la implementación de módulo de comunicación",
                entidad="UNIDAD EJECUTORA 002 INICTEL-UNI",
                fecha_limite=datetime.now(timezone.utc) + timedelta(hours=48),
                tiempo_restante_horas=48.0,
                estado_tiempo="amarillo",
                url_detalle="https://prod6.seace.gob.pe/buscador-publico/contrataciones/30527",
                fecha_publicacion=datetime.now(timezone.utc) - timedelta(hours=12)
            ),
            Contratacion(
                codigo="CM-154-2025-MDCH",
                descripcion="SERVICIO DE UN CONTADOR PROFESIONAL PARA FISCALIZACION",
                entidad="MUNICIPALIDAD DISTRITAL DE CHINCHAO",
                fecha_limite=datetime.now(timezone.utc) + timedelta(hours=96),
                tiempo_restante_horas=96.0,
                estado_tiempo="verde",
                url_detalle="https://prod6.seace.gob.pe/buscador-publico/contrataciones/30528",
                fecha_publicacion=datetime.now(timezone.utc) - timedelta(hours=6)
            ),
        ]

        return ContratacionResponse(
            contrataciones=contrataciones_muestra,
            total=len(contrataciones_muestra),
            timestamp=datetime.now(timezone.utc)
        )

        # TODO: Descomentar cuando se resuelva el issue de Playwright en Windows
        # username = os.getenv("user")
        # password = os.getenv("pass")
        # contrataciones = get_contrataciones(username, password)

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
