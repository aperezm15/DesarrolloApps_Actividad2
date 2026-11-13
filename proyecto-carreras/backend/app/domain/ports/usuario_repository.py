from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.usuario import Usuario


class UsuarioRepository(ABC):

    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario: ...

    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]: ...

    @abstractmethod
    def obtener_por_username(self, username: str) -> Optional[Usuario]: ...

    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]: ...

    @abstractmethod
    def listar(self) -> List[Usuario]: ...

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Optional[Usuario]: ...

    @abstractmethod
    def eliminar(self, usuario_id: int) -> bool: ...