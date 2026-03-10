from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from datetime import date 
from fastapi.security import HTTPBasic, HTTPBasicCredentials #<- importando el httpbasic,credentials#
import secrets

reservaciones=[]

class crear_reserva(BaseModel):
    id:int=Field(...,gt=0, description="Identificador de reserva")
    nombre:str=Field(...,max_length=6,description="Nombre del cliente (max 6 caracteres).)")
    fecha_reserva=date
    numero_personas=int=Field(...,)

@app.get("/reservaciones/listado")
async def listar_reservaciones():
    return{
        "total_reservaciones":len(reservaciones),
        "reservaciones:":reservaciones,
        "status:":"200"
    }

