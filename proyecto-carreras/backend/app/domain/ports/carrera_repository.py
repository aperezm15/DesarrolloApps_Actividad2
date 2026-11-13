from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.carrera import Carrera


class CarreraRepository(ABC):
    

    @abstractmethod
    def guardar(self, carrera: Carrera) -> Carrera: ...

    @abstractmethod
    def obtener_por_id(self, carrera_id: int) -> Optional[Carrera]: ...

    @abstractmethod
    def listar(self) -> List[Carrera]: ...

    @abstractmethod
    def actualizar(self, carrera: Carrera) -> Optional[Carrera]: ...

    @abstractmethod
    def eliminar(self, carrera_id: int) -> bool: ...