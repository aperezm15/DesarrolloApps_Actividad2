class CarreraNoEncontrada(Exception):

    def __init__(self, carrera_id: int):
        self.carrera_id = carrera_id
        super().__init__(f"No existe una carrera con id {carrera_id}")