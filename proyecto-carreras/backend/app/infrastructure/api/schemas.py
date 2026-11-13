from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CarreraBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=150)
    num_creditos: int = Field(gt=0)
    num_asignaturas: int = Field(gt=0)
    num_semestres: int = Field(gt=0)
    nivel_formacion: str = Field(min_length=3, max_length=50)
    titulo: str = Field(min_length=3, max_length=150)
    valor_semestre: float = Field(ge=0)
    universidad: str = Field(min_length=2, max_length=150)
    es_acreditada: bool
    perfiles: str = Field(min_length=1)
    area_conocimiento: str = Field(min_length=3, max_length=100)


class CarreraCrear(CarreraBase):
    pass



class CarreraRespuesta(CarreraBase):

    id: int
    model_config = ConfigDict(from_attributes=True)




class UsuarioCrear(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=72)
    nombre: str = Field(min_length=2, max_length=150)
    email: EmailStr


class UsuarioActualizar(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    nombre: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: Optional[str] = Field(default=None, min_length=6, max_length=72)


class UsuarioRespuesta(BaseModel):
    """Nunca incluye el password, ni siquiera el hash."""
    id: int
    username: str
    nombre: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)



class LoginRequest(BaseModel):
    username: str
    password: str


class LoginRespuesta(BaseModel):
    mensaje: str
    usuario: UsuarioRespuesta