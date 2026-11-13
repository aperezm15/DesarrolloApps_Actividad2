from dataclasses import dataclass
from typing import List, Optional

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

@dataclass
class ResultadoReporteCarreras:
    total: int
    promedio_valor_semestre: float
    carreras: List[Carrera]


def _resumir(carreras: List[Carrera]) -> ResultadoReporteCarreras:
    total = len(carreras)
    promedio = sum(c.valor_semestre for c in carreras) / total if total else 0.0
    return ResultadoReporteCarreras(
        total=total,
        promedio_valor_semestre=round(promedio, 2),
        carreras=carreras,
    )


class ReporteCarrerasPorNivel:
    def __init__(self, repo: CarreraRepository):
        self.repo = repo

    def ejecutar(
        self, nivel_formacion: str, valor_semestre_max: Optional[float] = None
    ) -> ResultadoReporteCarreras:
        return _resumir(self.repo.listar_por_nivel(nivel_formacion, valor_semestre_max))


class ReporteCarrerasPorAcreditacion:
    def __init__(self, repo: CarreraRepository):
        self.repo = repo

    def ejecutar(
        self, es_acreditada: bool, universidad: Optional[str] = None
    ) -> ResultadoReporteCarreras:
        return _resumir(self.repo.listar_por_acreditacion(es_acreditada, universidad))