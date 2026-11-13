from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    username: str
    password: str 
    nombre: str
    email: str
    id: Optional[int] = None