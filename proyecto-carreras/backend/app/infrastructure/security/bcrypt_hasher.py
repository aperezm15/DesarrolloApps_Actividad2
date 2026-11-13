import bcrypt

from app.domain.ports.password_hasher import PasswordHasher


class BcryptHasher(PasswordHasher):
    """Adaptador de salida: implementa el puerto con bcrypt."""

    def hashear(self, clave: str) -> str:
        return bcrypt.hashpw(clave.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verificar(self, clave: str, hash_guardado: str) -> bool:
        try:
            return bcrypt.checkpw(clave.encode("utf-8"), hash_guardado.encode("utf-8"))
        except ValueError:
            return False