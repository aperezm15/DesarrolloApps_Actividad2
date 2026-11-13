from fastapi import APIRouter, Depends, HTTPException

from app.application.use_cases.usuario_use_cases import Login
from app.domain.exceptions import CredencialesInvalidas
from app.domain.ports.password_hasher import PasswordHasher
from app.domain.ports.usuario_repository import UsuarioRepository
from app.infrastructure.api.schemas import LoginRequest, LoginRespuesta
from app.infrastructure.api.usuario_router import get_hasher, get_repo

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=LoginRespuesta)
def login(
    datos: LoginRequest,
    repo: UsuarioRepository = Depends(get_repo),
    hasher: PasswordHasher = Depends(get_hasher),
):
    try:
        usuario = Login(repo, hasher).ejecutar(datos.username, datos.password)
    except CredencialesInvalidas as e:
        raise HTTPException(status_code=401, detail=str(e))
    return LoginRespuesta(mensaje="Inicio de sesión exitoso", usuario=usuario)