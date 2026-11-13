from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from sqlalchemy.orm import Session

from app.application.use_cases.carrera_use_cases import (
    ActualizarCarrera,
    CrearCarrera,
    EliminarCarrera,
    ListarCarreras,
    ObtenerCarrera,
)
from app.domain.entities.carrera import Carrera
from app.domain.exceptions import CarreraNoEncontrada
from app.domain.ports.carrera_repository import CarreraRepository
from app.infrastructure.api.schemas import CarreraCrear, CarreraRespuesta
from app.infrastructure.persistence.carrera_repository_sql import CarreraRepositorySQL
from app.infrastructure.persistence.database import get_db

from app.application.use_cases.carrera_use_cases import (
    ActualizarCarrera,
    CrearCarrera,
    EliminarCarrera,
    ListarCarreras,
    ObtenerCarrera,
    ReporteCarrerasPorAcreditacion,
    ReporteCarrerasPorNivel,
)
from app.infrastructure.api.schemas import (
    CarreraCrear,
    CarreraRespuesta,
    ReporteCarrerasRespuesta,
)

router = APIRouter(prefix="/carreras", tags=["Carreras"])


def get_repo(db: Session = Depends(get_db)) -> CarreraRepository:
    return CarreraRepositorySQL(db)


@router.post("", response_model=CarreraRespuesta, status_code=status.HTTP_201_CREATED)
def crear_carrera(datos: CarreraCrear, repo: CarreraRepository = Depends(get_repo)):
    carrera = Carrera(**datos.model_dump())
    return CrearCarrera(repo).ejecutar(carrera)


@router.get("", response_model=List[CarreraRespuesta])
def listar_carreras(repo: CarreraRepository = Depends(get_repo)):
    return ListarCarreras(repo).ejecutar()


@router.get("/{carrera_id}", response_model=CarreraRespuesta)
def obtener_carrera(carrera_id: int, repo: CarreraRepository = Depends(get_repo)):
    try:
        return ObtenerCarrera(repo).ejecutar(carrera_id)
    except CarreraNoEncontrada as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{carrera_id}", response_model=CarreraRespuesta)
def actualizar_carrera(
    carrera_id: int, datos: CarreraCrear, repo: CarreraRepository = Depends(get_repo)
):
    try:
        carrera = Carrera(**datos.model_dump())
        return ActualizarCarrera(repo).ejecutar(carrera_id, carrera)
    except CarreraNoEncontrada as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{carrera_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_carrera(carrera_id: int, repo: CarreraRepository = Depends(get_repo)):
    try:
        EliminarCarrera(repo).ejecutar(carrera_id)
    except CarreraNoEncontrada as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/reportes/por-nivel", response_model=ReporteCarrerasRespuesta)
def reporte_por_nivel(
    nivel_formacion: str = Query(..., min_length=3, description="Ej: Pregrado"),
    valor_semestre_max: Optional[float] = Query(None, ge=0),
    repo: CarreraRepository = Depends(get_repo),
):
    return ReporteCarrerasPorNivel(repo).ejecutar(nivel_formacion, valor_semestre_max)


@router.get("/reportes/por-acreditacion", response_model=ReporteCarrerasRespuesta)
def reporte_por_acreditacion(
    es_acreditada: bool = Query(..., description="true o false"),
    universidad: Optional[str] = Query(None, description="Texto parcial del nombre"),
    repo: CarreraRepository = Depends(get_repo),
):
    return ReporteCarrerasPorAcreditacion(repo).ejecutar(es_acreditada, universidad)