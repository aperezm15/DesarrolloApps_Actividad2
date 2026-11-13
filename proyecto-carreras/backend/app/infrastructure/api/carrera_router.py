from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
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