from fastapi import FastAPI, status, HTTPException
from typing import Optional 
import asyncio

app = FastAPI()

usuarios=[
    {"id":1,"nombre":"Fany","edad":21},
    {"id":2,"nombre":"Ali","edad":21},
    {"id":3,"nombre":"Dulce","edad":21},
]

@app.get("/")
async def holamundo(): 
    return {"mensaje": "Hola mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido(): 
    await asyncio.sleep(5)
    return {"mensaje": "Bienvenido a FastAPI"}


@app.get("/usuario/detalles")
async def detalles(nombre: str, edad: int):
    return {"nombre":nombre, "edad": edad}



@app.get("/v1/usuarios/",tags=['HTTP CRUD'])
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "usuarios":usuarios,
        "status": "200"
    }

@app.post("/v1/usuarios/",tags=['HTTP CRUD'])
async def agregar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
        
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Creado",
        "Datos nuevos": usuario,
    }

@app.put("/v1/usuarios/",tags=['HTTP CRUD'])
async def actualizar_usuario(usuario_id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario_id:
            usr.update(usuario)
            return{
                "mensaje": "Usuario Actualizado",
                "Datos actualizados": usr,
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.patch("/v1/usuarios/",tags=['HTTP CRUD'])
async def modificar_usuario(usuario_id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario_id:
            usr.update(usuario)
            return{
                "mensaje": "Usuario Modificado",
                "Datos modificados": usr,
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/1",tags=['HTTP CRUD'])
async def eliminar_usuario(usuario_id: int):
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios.pop(i)
            return{
                "mensaje": "Usuario Eliminado",
                "id eliminado": usuario_id,
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

