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


@router.put("/{usuario_id}",tags=['HTTP CRUD'])
async def actualizar_usuario(usuario_id: int, usuario: crear_usuario, db:Session= Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    usuario_db.nombre = usuario.nombre
    usuario_db.edad = usuario.edad
    db.commit()
    db.refresh(usuario_db)
    
    return{
        "mensaje": "Usuario Actualizado",
        "Datos actualizados": usuario_db,
    }

@router.patch("/{usuario_id}",tags=['HTTP CRUD'])
async def modificar_usuario(usuario_id: int, usuario: dict, db:Session= Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    if "nombre" in usuario:
        usuario_db.nombre = usuario["nombre"]
    if "edad" in usuario:
        usuario_db.edad = usuario["edad"]
    
    db.commit()
    db.refresh(usuario_db)
    
    return{
        "mensaje": "Usuario Modificado",
        "Datos modificados": usuario_db,
    }

@router.delete("/{usuario_id}",tags=['HTTP CRUD'])
async def eliminar_usuario(usuario_id: int, db:Session= Depends(get_db), usuarioAuth:str=Depends(verificar_peticion)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    db.delete(usuario_db)
    db.commit()
    
    return{
        "mensaje": f"Usuario Eliminado por {usuarioAuth}",
        "id eliminado": usuario_id,
    }


