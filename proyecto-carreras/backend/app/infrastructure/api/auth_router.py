from fastapi import APIRouter, Depends, HTTPException

from app.application.use_cases.usuario_use_cases import Login, RecordarClave
from app.domain.exceptions import CredencialesInvalidas, ErrorEnvioCorreo
from app.domain.ports.email_sender import EmailSender
from app.domain.ports.password_hasher import PasswordHasher
from app.domain.ports.usuario_repository import UsuarioRepository
from app.infrastructure.api.schemas import (
    LoginRequest,
    LoginRespuesta,
    MensajeRespuesta,
    RecuperarClaveRequest,
)
from app.infrastructure.api.usuario_router import get_hasher, get_repo
from app.infrastructure.email.factory import get_email_sender

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


@router.post("/recuperar-clave", response_model=MensajeRespuesta)
def recuperar_clave(
    datos: RecuperarClaveRequest,
    repo: UsuarioRepository = Depends(get_repo),
    hasher: PasswordHasher = Depends(get_hasher),
    email_sender: EmailSender = Depends(get_email_sender),
):
    try:
        RecordarClave(repo, hasher, email_sender).ejecutar(datos.email)
    except ErrorEnvioCorreo:
        raise HTTPException(
            status_code=503,
            detail="No fue posible enviar el correo. Intenta más tarde.",
        )
    return MensajeRespuesta(
        mensaje="Si el correo está registrado, recibirás una clave temporal."
    )