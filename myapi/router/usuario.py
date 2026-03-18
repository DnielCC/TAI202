from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from myapi.models.usuario import crear_usuario
from myapi.data.database import usuarios 
from myapi.security.auth import verificar_peticion


router=APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]

) 


@router.get("/",tags=['HTTP CRUD'])
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "usuarios":usuarios,
        "status": "200"
    }

    
@router.post("/",tags=['HTTP CRUD'])
async def agregar_usuarios(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id: 
            raise HTTPException(
                status_code=400,
                detail="El usuario con este ID ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje":"Usuario Agregado",
        "Datos nuevos":usuario
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


