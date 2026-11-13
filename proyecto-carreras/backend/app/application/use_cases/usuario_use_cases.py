import secrets
import string
from dataclasses import dataclass
from typing import List, Optional

from app.domain.entities.usuario import Usuario
from app.domain.exceptions import (
    CredencialesInvalidas,
    UsuarioDuplicado,
    UsuarioNoEncontrado,
)
from app.domain.ports.password_hasher import PasswordHasher
from app.domain.ports.usuario_repository import UsuarioRepository

from app.domain.entities.usuario import Usuario
from app.domain.exceptions import (
    CredencialesInvalidas,
    ErrorEnvioCorreo,
    UsuarioDuplicado,
    UsuarioNoEncontrado,
)
from app.domain.ports.email_sender import EmailSender
from app.domain.ports.password_hasher import PasswordHasher
from app.domain.ports.usuario_repository import UsuarioRepository


class CrearUsuario:
    def __init__(self, repo: UsuarioRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    def ejecutar(self, usuario: Usuario) -> Usuario:
        usuario.email = usuario.email.strip().lower()
        if self.repo.obtener_por_username(usuario.username):
            raise UsuarioDuplicado("username")
        if self.repo.obtener_por_email(usuario.email):
            raise UsuarioDuplicado("email")
        usuario.password = self.hasher.hashear(usuario.password)
        return self.repo.guardar(usuario)


class ObtenerUsuario:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, usuario_id: int) -> Usuario:
        usuario = self.repo.obtener_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNoEncontrado(usuario_id)
        return usuario


class ListarUsuarios:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self) -> List[Usuario]:
        return self.repo.listar()


class ActualizarUsuario:
    def __init__(self, repo: UsuarioRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    def ejecutar(
        self,
        usuario_id: int,
        username: str,
        nombre: str,
        email: str,
        nueva_password: Optional[str] = None,
    ) -> Usuario:
        actual = self.repo.obtener_por_id(usuario_id)
        if actual is None:
            raise UsuarioNoEncontrado(usuario_id)

        email = email.strip().lower()
        otro = self.repo.obtener_por_username(username)
        if otro and otro.id != usuario_id:
            raise UsuarioDuplicado("username")
        otro = self.repo.obtener_por_email(email)
        if otro and otro.id != usuario_id:
            raise UsuarioDuplicado("email")

        actual.username = username
        actual.nombre = nombre
        actual.email = email
        if nueva_password:
            actual.password = self.hasher.hashear(nueva_password)

        actualizado = self.repo.actualizar(actual)
        if actualizado is None:
            raise UsuarioNoEncontrado(usuario_id)
        return actualizado


class EliminarUsuario:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, usuario_id: int) -> None:
        if not self.repo.eliminar(usuario_id):
            raise UsuarioNoEncontrado(usuario_id)


class Login:
    def __init__(self, repo: UsuarioRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    def ejecutar(self, username: str, password: str) -> Usuario:
        usuario = self.repo.obtener_por_username(username)
        if usuario is None or not self.hasher.verificar(password, usuario.password):
            raise CredencialesInvalidas()
        return usuario

class ResultadoReporteUsuarios:
    total: int
    usuarios: List[Usuario]


class ReporteUsuariosPorNombre:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, nombre: str) -> ResultadoReporteUsuarios:
        usuarios = self.repo.buscar_por_nombre(nombre)
        return ResultadoReporteUsuarios(total=len(usuarios), usuarios=usuarios)


class ReporteUsuariosPorDominio:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, dominio: str) -> ResultadoReporteUsuarios:
        usuarios = self.repo.listar_por_dominio_email(dominio)
        return ResultadoReporteUsuarios(total=len(usuarios), usuarios=usuarios)

class RecordarClave:
    def __init__(
        self,
        repo: UsuarioRepository,
        hasher: PasswordHasher,
        email_sender: EmailSender,
    ):
        self.repo = repo
        self.hasher = hasher
        self.email_sender = email_sender

    @staticmethod
    def _generar_clave(longitud: int = 10) -> str:
        # Sin caracteres ambiguos (0/O, 1/l/I) para que sea fácil de leer
        alfabeto = "".join(
            c for c in string.ascii_letters + string.digits if c not in "0O1lI"
        )
        return "".join(secrets.choice(alfabeto) for _ in range(longitud))

    def ejecutar(self, email: str) -> None:
        usuario = self.repo.obtener_por_email(email.strip().lower())
        if usuario is None:
            return  # silencio a propósito: no revelamos si el correo existe

        clave_temporal = self._generar_clave()
        hash_anterior = usuario.password
        usuario.password = self.hasher.hashear(clave_temporal)
        self.repo.actualizar(usuario)

        cuerpo = (
            f"Hola {usuario.nombre},\n\n"
            f"Recibimos una solicitud para recuperar tu clave.\n"
            f"Tu clave temporal es: {clave_temporal}\n\n"
            f"Inicia sesión con ella y cámbiala lo antes posible.\n"
            f"Si no fuiste tú, avisa al administrador."
        )
        try:
            self.email_sender.enviar(usuario.email, "Recuperación de clave", cuerpo)
        except ErrorEnvioCorreo:
            # Si el correo no salió, se restaura la clave anterior
            usuario.password = hash_anterior
            self.repo.actualizar(usuario)
            raise