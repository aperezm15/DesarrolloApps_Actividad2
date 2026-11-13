from dataclasses import asdict
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.usuario import Usuario
from app.domain.ports.usuario_repository import UsuarioRepository
from app.infrastructure.persistence.models import UsuarioModel


class UsuarioRepositorySQL(UsuarioRepository):

    def __init__(self, db: Session):
        self.db = db

    def _a_entidad(self, m: UsuarioModel) -> Usuario:
        return Usuario(
            id=m.id,
            username=m.username,
            password=m.password,
            nombre=m.nombre,
            email=m.email,
        )

    def guardar(self, usuario: Usuario) -> Usuario:
        datos = asdict(usuario)
        datos.pop("id", None)
        modelo = UsuarioModel(**datos)
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._a_entidad(modelo)

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        modelo = self.db.get(UsuarioModel, usuario_id)
        return self._a_entidad(modelo) if modelo else None

    def obtener_por_username(self, username: str) -> Optional[Usuario]:
        modelo = (
            self.db.query(UsuarioModel).filter(UsuarioModel.username == username).first()
        )
        return self._a_entidad(modelo) if modelo else None

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        modelo = self.db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
        return self._a_entidad(modelo) if modelo else None

    def listar(self) -> List[Usuario]:
        modelos = self.db.query(UsuarioModel).order_by(UsuarioModel.id).all()
        return [self._a_entidad(m) for m in modelos]

    def actualizar(self, usuario: Usuario) -> Optional[Usuario]:
        modelo = self.db.get(UsuarioModel, usuario.id)
        if modelo is None:
            return None
        modelo.username = usuario.username
        modelo.password = usuario.password
        modelo.nombre = usuario.nombre
        modelo.email = usuario.email
        self.db.commit()
        self.db.refresh(modelo)
        return self._a_entidad(modelo)

    def eliminar(self, usuario_id: int) -> bool:
        modelo = self.db.get(UsuarioModel, usuario_id)
        if modelo is None:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def buscar_por_nombre(self, nombre: str) -> List[Usuario]:
        modelos = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.nombre.ilike(f"%{nombre.strip()}%"))
            .order_by(UsuarioModel.nombre)
            .all()
        )
        return [self._a_entidad(m) for m in modelos]

    def listar_por_dominio_email(self, dominio: str) -> List[Usuario]:
        dominio = dominio.strip().lower().lstrip("@")
        modelos = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.email.ilike(f"%@{dominio}"))
            .order_by(UsuarioModel.email)
            .all()
        )
        return [self._a_entidad(m) for m in modelos]