from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Optional
from pydantic import BaseModel,Field,field_validator
from datetime import date, datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials #<- importando el httpbasic,credentials#
import secrets

app = FastAPI()
reservaciones=[
    {
    "id":1,
    "nombre":"eros",
    "fecha":"26-01-10",
    "numero de personas":3
}
]


class crear_reserva(BaseModel):
    id:int=Field(...,gt=0, description="Identificador de reserva")
    nombre:str=Field(...,max_length=6,description="Nombre del cliente (max 6 caracteres).)")
    fecha_reserva:date
    numero_personas:int=Field(...,ge=1,le=10,description="numero de personas minimo 1, maximo 6")

@field_validator("fecha_reserva")
@classmethod
def validar_no_futura(cls,v: datetime):
    ahora=datetime.now()
    if v <= ahora:
        raise ValueError("la fecha no se puede ser en el futuro")

    if v.weekday()==6:
        raise ValueError("La reservación no se puede hacer en domingo")
    
    hora_inicio = time(8, 0)
    hora_fin = time(22, 0) 
    if not (hora_inicio <= v.time() <= hora_fin):
        raise ValueError(f'El horario de atención es de {hora_inicio} a {hora_fin}.')

    return v

    
    
    

@app.get("/reservaciones/listado")
async def listar_reservaciones():
    return{
        "total_reservaciones":len(reservaciones),
        "reservaciones:":reservaciones,
        "status:":"200"
    }

@app.post("/reservaciones/crear_reserva")
async def crear_reservacion(reservacion:crear_reserva):
    for rsv in reservacion:
        if rsv["id"] == reservacion.id:
            raise HTTPException(
                status_code=400,
                detail="La reservacion con este ID ya existe"
            )
    reservacion.append(reservacion)
    return{
        "mensaje":"reservacion agregada",
        "datos nuevos": reservacion
    }
    
@app.get("/reservaciones/consulta")
async def consulta_reservacion(id:int):
    for id in reservaciones:
        if id == reservaciones:
            return reservaciones

