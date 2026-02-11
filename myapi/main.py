from fastapi import FastAPI
from typing import Optional 
import asyncio

app = FastAPI()


@app.get("/")
async def holamundo(): 
    return {"mensaje": "Hola mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido(): 
    await asyncio.sleep(5)
    return {"mensaje": "Bienvenido a FastAPI"}


# --- Práctica 2: Parámetros Obligatorios ---
# Se definen en la misma URL entre llaves {param}
@app.get("/usuario/{id}")
async def leer_usuario(id: int):
    return {
        "mensaje": f"Has consultado al usuario con ID: {id}",
        "tipo_parametro": "obligatorio (path parameter)"
    }

# --- Práctica 2: Parámetros Opcionales ---
# Se definen en los argumentos de la función (query parameters)
@app.get("/busqueda/")
async def buscar_item(nombre: str, calificacion: Optional[float] = None):
    return {
        "mensaje": f"Buscando: {nombre}",
        "calificacion_filtro": calificacion if calificacion else "No se proporcionó calificación",
        "tipo_parametro": "opcional (query parameter)"
    }