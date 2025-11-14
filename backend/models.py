from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class Contratacion(BaseModel):
    codigo: str
    descripcion: str
    entidad: str
    fecha_limite: datetime
    tiempo_restante_horas: float
    estado_tiempo: Literal["rojo", "amarillo", "verde"]
    url_detalle: str
    fecha_publicacion: datetime | None = None


class ContratacionResponse(BaseModel):
    contrataciones: list[Contratacion]
    total: int
    timestamp: datetime
