from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from myapi.models.usuario import crear_usuario
from myapi.data.database import usuarios 
from myapi.security.auth import verificar_peticion
from sqlalchemy.orm import Session
from myapi.data.db import get_db
from myapi.data.usuarios import usuario as dbUsuario

router=APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]

) 


@router.get("/",tags=['HTTP CRUD'])
async def leer_usuarios(db:Session= Depends(get_db)):
    queryUsuarios= db.query(dbUsuario).all()
    return{
        "total":len(queryUsuarios),
        "usuarios":queryUsuarios,
        "status": "200"
    }

    
@router.post("/",tags=['HTTP CRUD'])
async def agregar_usuarios(usuarioP:crear_usuario,db:Session= Depends(get_db)):
    nuevoU= dbUsuario(nombre= usuarioP.nombre, edad= usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)
     
    return {
        "mensaje":"Usuario Agregado",
        "Datos nuevos":usuarioP
    }


@router.put("/",tags=['HTTP CRUD'])
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

@router.patch("/",tags=['HTTP CRUD'])
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

@router.delete("/",tags=['HTTP CRUD'])
async def eliminar_usuario(usuario_id: int,usuarioAuth:str=Depends(verificar_peticion)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios.pop(i)
            return{
                "mensaje": f"Usuario Eliminado por {usuarioAuth}",
                "id eliminado": usuario_id,
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


