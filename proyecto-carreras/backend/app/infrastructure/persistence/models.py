from sqlalchemy import Boolean, Column, Float, Integer, String, Text

from app.infrastructure.persistence.database import Base


class CarreraModel(Base):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    num_creditos = Column(Integer, nullable=False)
    num_asignaturas = Column(Integer, nullable=False)
    num_semestres = Column(Integer, nullable=False)
    nivel_formacion = Column(String(50), nullable=False, index=True)
    titulo = Column(String(150), nullable=False)
    valor_semestre = Column(Float, nullable=False)
    universidad = Column(String(150), nullable=False, index=True)
    es_acreditada = Column(Boolean, nullable=False, default=False)
    perfiles = Column(Text, nullable=False)
    area_conocimiento = Column(String(100), nullable=False)