
from fastapi import FastAPI
from myapi.router import usuario, misc
from myapi.data.db import engine
from myapi.data import usuarios as UsuarioDB

UsuarioDB.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(usuario.router)
app.include_router(misc.misc)




from pydantic import BaseModel, field_validator
from datetime import datetime

class Reservacion(BaseModel):
    id: int
    nombre: str
    # Usamos datetime para tener fecha y hora en un solo campo
    fecha_cita: datetime 

    @field_validator("fecha_cita")
    @classmethod
    def validar_reglas_horario(cls, v: datetime):
        # --- 1. VALIDACIÓN DE DÍA (No domingos) ---
        # .weekday() devuelve: 0=Lunes, 1=Martes ... 5=Sábado, 6=Domingo
        if v.weekday() == 6:
            raise ValueError("Lo sentimos, no abrimos los domingos.")

        # --- 2. VALIDACIÓN DE HORA (Rangos 13-14 y 16-22) ---
        hora = v.hour # Extrae solo la hora (0 a 23)
        
        # Definimos los rangos permitidos
        bloque_almuerzo = (13 <= hora < 14)  # De 1:00 PM a 1:59 PM
        bloque_tarde = (16 <= hora < 22)     # De 4:00 PM a 9:59 PM

        if not (bloque_almuerzo or bloque_tarde):
            raise ValueError("Horario no disponible. Solo atendemos de 1-2 PM y 4-10 PM.")

        return v


    #/Solo números (e.g., ID de 5 dígitos): pattern=r"^\d{5}$"

#Solo letras (sin espacios): pattern=r"^[a-zA-Z]+$"

#Formato de teléfono simple: pattern=r"^\d{10}$"#/