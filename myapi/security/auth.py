from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials #<- importando el httpbasic,credentials#
import secrets


#seguridad HTTP BASIC
security= HTTPBasic()


#Funcion para corroborar las credenciales
def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuario_correcto=secrets.compare_digest(credenciales.username,"eros")
    contrasena_correcta=secrets.compare_digest(credenciales.password,"123456")

    if not(usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales no validas"
        )
    return credenciales.username 
