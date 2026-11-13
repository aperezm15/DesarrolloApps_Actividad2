from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Puerto de salida: cifrar y verificar contraseñas."""

    @abstractmethod
    def hashear(self, clave: str) -> str: ...

    @abstractmethod
    def verificar(self, clave: str, hash_guardado: str) -> bool: ...