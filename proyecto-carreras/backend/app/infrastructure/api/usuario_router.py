from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.application.use_cases.usuario_use_cases import (
    ActualizarUsuario,
    CrearUsuario,
    EliminarUsuario,
    ListarUsuarios,
    ObtenerUsuario,
)
from app.domain.entities.usuario import Usuario
from app.domain.exceptions import UsuarioDuplicado, UsuarioNoEncontrado
from app.domain.ports.password_hasher import PasswordHasher
from app.domain.ports.usuario_repository import UsuarioRepository
from app.infrastructure.api.schemas import (
    UsuarioActualizar,
    UsuarioCrear,
    UsuarioRespuesta,
)
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.usuario_repository_sql import UsuarioRepositorySQL
from app.infrastructure.security.bcrypt_hasher import BcryptHasher

from app.application.use_cases.usuario_use_cases import (
    ActualizarUsuario,
    CrearUsuario,
    EliminarUsuario,
    ListarUsuarios,
    ObtenerUsuario,
    ReporteUsuariosPorDominio,
    ReporteUsuariosPorNombre,
)
from app.infrastructure.api.schemas import (
    ReporteUsuariosRespuesta,
    UsuarioActualizar,
    UsuarioCrear,
    UsuarioRespuesta,
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_repo(db: Session = Depends(get_db)) -> UsuarioRepository:
    return UsuarioRepositorySQL(db)


def get_hasher() -> PasswordHasher:
    return BcryptHasher()


@router.post("", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    datos: UsuarioCrear,
    repo: UsuarioRepository = Depends(get_repo),
    hasher: PasswordHasher = Depends(get_hasher),
):
    try:
        usuario = Usuario(**datos.model_dump())
        return CrearUsuario(repo, hasher).ejecutar(usuario)
    except UsuarioDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("", response_model=List[UsuarioRespuesta])
def listar_usuarios(repo: UsuarioRepository = Depends(get_repo)):
    return ListarUsuarios(repo).ejecutar()


@router.get("/{usuario_id}", response_model=UsuarioRespuesta)
def obtener_usuario(usuario_id: int, repo: UsuarioRepository = Depends(get_repo)):
    try:
        return ObtenerUsuario(repo).ejecutar(usuario_id)
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{usuario_id}", response_model=UsuarioRespuesta)
def actualizar_usuario(
    usuario_id: int,
    datos: UsuarioActualizar,
    repo: UsuarioRepository = Depends(get_repo),
    hasher: PasswordHasher = Depends(get_hasher),
):
    try:
        return ActualizarUsuario(repo, hasher).ejecutar(
            usuario_id,
            datos.username,
            datos.nombre,
            datos.email,
            datos.password,
        )
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UsuarioDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, repo: UsuarioRepository = Depends(get_repo)):
    try:
        EliminarUsuario(repo).ejecutar(usuario_id)
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/reportes/por-nombre", response_model=ReporteUsuariosRespuesta)
def reporte_por_nombre(
    nombre: str = Query(..., min_length=1),
    repo: UsuarioRepository = Depends(get_repo),
):
    return ReporteUsuariosPorNombre(repo).ejecutar(nombre)


@router.get("/reportes/por-dominio", response_model=ReporteUsuariosRespuesta)
def reporte_por_dominio(
    dominio: str = Query(..., min_length=3, description="Ej: gmail.com"),
    repo: UsuarioRepository = Depends(get_repo),
):
    return ReporteUsuariosPorDominio(repo).ejecutar(dominio)