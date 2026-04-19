from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List

app = FastAPI()
security = HTTPBasic()

# --- 1. SEGURIDAD SIMPLE ---
def validar_usuario(credenciales: HTTPBasicCredentials = Depends(security)):
    # Usuario y contraseña quemados para el ejemplo
    if credenciales.username != "profe" or credenciales.password != "1234":
        raise HTTPException(status_code=401, detail="No autorizado")
    return credenciales.username

# --- 2. MODELO DE DATOS (PYDANTIC) ---
class Reservacion(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2)
    apellido: str = Field(..., min_length=2)
    fecha: date
    estado: str = "Activa" # Estados: Activa, Pendiente Cancelar, Cancelada

    # Validación: Solo un nombre y un apellido
    @field_validator("nombre", "apellido")
    @classmethod
    def validar_un_solo_termino(cls, valor: str):
        if len(valor.split()) > 1:
            raise ValueError("Solo se permite UN nombre/apellido (sin espacios)")
        return valor

# --- 3. BASE DE DATOS EN MEMORIA ---
db: List[Reservacion] = []

# --- 4. ENDPOINTS ---

# Crear reservación
@app.post("/reservar", dependencies=[Depends(validar_usuario)])
def crear(res: Reservacion):
    db.append(res)
    return {"msg": "Registrada", "data": res}

# Listar todas
@app.get("/reservaciones", dependencies=[Depends(validar_usuario)])
def listar():
    return db

# Buscar por ID
@app.get("/reservacion/{id_buscado}", dependencies=[Depends(validar_usuario)])
def buscar(id_buscado: int):
    for r in db:
        if r.id == id_buscado:
            return r
    raise HTTPException(status_code=404, detail="No encontrada")

# Mostrar lista de clientes únicos
@app.get("/clientes", dependencies=[Depends(validar_usuario)])
def mostrar_clientes():
    # Creamos un set para evitar duplicados
    clientes = {f"{r.nombre} {r.apellido}" for r in db}
    return {"clientes": list(clientes)}

# PASO 1: Solicitar cancelación
@app.put("/cancelar/solicitar/{id_res}", dependencies=[Depends(validar_usuario)])
def solicitar_cancelacion(id_res: int):
    for r in db:
        if r.id == id_res:
            r.estado = "Pendiente Cancelar"
            return {"msg": "Solicitud recibida"}
    raise HTTPException(status_code=404, detail="No encontrada")

# PASO 2: Confirmar cancelación
@app.put("/cancelar/confirmar/{id_res}", dependencies=[Depends(validar_usuario)])
def confirmar_cancelacion(id_res: int):
    for r in db:
        if r.id == id_res and r.estado == "Pendiente Cancelar":
            r.estado = "Cancelada"
            return {"msg": "Cancelación confirmada"}
    raise HTTPException(status_code=400, detail="No se puede confirmar o no existe")