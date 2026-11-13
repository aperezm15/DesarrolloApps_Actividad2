from typing import List

from app.domain.entities.carrera import Carrera
from app.domain.exceptions import CarreraNoEncontrada
from app.domain.ports.carrera_repository import CarreraRepository


class CrearCarrera:
    def __init__(self, repo: CarreraRepository):
        self.repo = repo

    def ejecutar(self, carrera: Carrera) -> Carrera:
        return self.repo.guardar(carrera)


class ObtenerCarrera:
    def __init__(self, repo: CarreraRepository):
        self.repo = repo

    def ejecutar(self, carrera_id: int) -> Carrera:
        carrera = self.repo.obtener_por_id(carrera_id)
        if carrera is None:
            raise CarreraNoEncontrada(carrera_id)
        return carrera


class ListarCarreras:
    def __init__(self, repo: CarreraRepository):
        self.repo = repo

    def ejecutar(self) -> List[Carrera]:
        return self.repo.listar()


class ActualizarCarrera:
    def __init__(self, repo: CarreraRepository):
        self.repo = repo

    def ejecutar(self, carrera_id: int, carrera: Carrera) -> Carrera:
        carrera.id = carrera_id
        actualizada = self.repo.actualizar(carrera)
        if actualizada is None:
            raise CarreraNoEncontrada(carrera_id)
        return actualizada


class EliminarCarrera:
    def __init__(self, repo: CarreraRepository):
        self.repo = repo

    def ejecutar(self, carrera_id: int) -> None:
        if not self.repo.eliminar(carrera_id):
            raise CarreraNoEncontrada(carrera_id)