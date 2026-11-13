from dataclasses import asdict
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.entities.carrera import Carrera
from app.domain.ports.carrera_repository import CarreraRepository
from app.infrastructure.persistence.models import CarreraModel


class CarreraRepositorySQL(CarreraRepository):

    def __init__(self, db: Session):
        self.db = db

    def _a_entidad(self, m: CarreraModel) -> Carrera:
        return Carrera(
            id=m.id,
            nombre=m.nombre,
            num_creditos=m.num_creditos,
            num_asignaturas=m.num_asignaturas,
            num_semestres=m.num_semestres,
            nivel_formacion=m.nivel_formacion,
            titulo=m.titulo,
            valor_semestre=m.valor_semestre,
            universidad=m.universidad,
            es_acreditada=m.es_acreditada,
            perfiles=m.perfiles,
            area_conocimiento=m.area_conocimiento,
        )

    def guardar(self, carrera: Carrera) -> Carrera:
        datos = asdict(carrera)
        datos.pop("id", None)
        modelo = CarreraModel(**datos)
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)   
        return self._a_entidad(modelo)

    def obtener_por_id(self, carrera_id: int) -> Optional[Carrera]:
        modelo = self.db.get(CarreraModel, carrera_id)
        return self._a_entidad(modelo) if modelo else None

    def listar(self) -> List[Carrera]:
        modelos = self.db.query(CarreraModel).order_by(CarreraModel.id).all()
        return [self._a_entidad(m) for m in modelos]

    def actualizar(self, carrera: Carrera) -> Optional[Carrera]:
        modelo = self.db.get(CarreraModel, carrera.id)
        if modelo is None:
            return None
        datos = asdict(carrera)
        datos.pop("id", None)
        for campo, valor in datos.items():
            setattr(modelo, campo, valor)
        self.db.commit()
        self.db.refresh(modelo)
        return self._a_entidad(modelo)

    def eliminar(self, carrera_id: int) -> bool:
        modelo = self.db.get(CarreraModel, carrera_id)
        if modelo is None:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def listar_por_nivel(
        self, nivel_formacion: str, valor_semestre_max: Optional[float] = None
    ) -> List[Carrera]:
        consulta = self.db.query(CarreraModel).filter(
            func.lower(CarreraModel.nivel_formacion) == nivel_formacion.strip().lower()
        )
        if valor_semestre_max is not None:
            consulta = consulta.filter(CarreraModel.valor_semestre <= valor_semestre_max)
        modelos = consulta.order_by(CarreraModel.nombre).all()
        return [self._a_entidad(m) for m in modelos]

    def listar_por_acreditacion(
        self, es_acreditada: bool, universidad: Optional[str] = None
    ) -> List[Carrera]:
        consulta = self.db.query(CarreraModel).filter(
            CarreraModel.es_acreditada == es_acreditada
        )
        if universidad and universidad.strip():
            consulta = consulta.filter(
                CarreraModel.universidad.ilike(f"%{universidad.strip()}%")
            )
        modelos = consulta.order_by(CarreraModel.nombre).all()
        return [self._a_entidad(m) for m in modelos]