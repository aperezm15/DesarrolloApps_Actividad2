from dataclasses import dataclass
from typing import Optional


@dataclass
class Carrera:
    nombre: str
    num_creditos: int
    num_asignaturas: int
    num_semestres: int
    nivel_formacion: str      
    titulo: str
    valor_semestre: float
    universidad: str
    es_acreditada: bool
    perfiles: str
    area_conocimiento: str
    id: Optional[int] = None  