from fastapi import FastAPI

app = FastAPI(
    title="API Carreras",
    description="Backend con arquitectura hexagonal para la app Kodular",
    version="1.0.0",
)


@app.get("/")
def estado():
    return {"mensaje": "API de Carreras funcionando"}