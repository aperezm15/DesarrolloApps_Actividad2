class CarreraNoEncontrada(Exception):

    def __init__(self, carrera_id: int):
        self.carrera_id = carrera_id
        super().__init__(f"No existe una carrera con id {carrera_id}")


class UsuarioNoEncontrado(Exception):
    def __init__(self, usuario_id: int):
        self.usuario_id = usuario_id
        super().__init__(f"No existe un usuario con id {usuario_id}")


class UsuarioDuplicado(Exception):
    """El username o el email ya están registrados."""

    def __init__(self, campo: str):
        self.campo = campo
        super().__init__(f"Ya existe un usuario con ese {campo}")


class CredencialesInvalidas(Exception):
    def __init__(self):
        super().__init__("Usuario o contraseña incorrectos")