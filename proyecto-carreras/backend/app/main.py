from fastapi import FastAPI

from app.infrastructure.api.carrera_router import router as carrera_router
from app.infrastructure.persistence import models
from app.infrastructure.persistence.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Carreras",
    description="Backend con arquitectura hexagonal para la app Kodular",
    version="1.0.0",
)

app.include_router(carrera_router)


@app.get("/")
def estado():
    return {"mensaje": "API de Carreras funcionando"}