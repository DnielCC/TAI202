from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel


SECRET_KEY = "UPQ_SISTEMAS_KEY" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Activa el botón Authorize

app = FastAPI()


users_db = {"admin": {"username": "admin", "password": "123"}}

# --- b. Generación de Tokens ---
def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


async def check_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token no válido")

@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if not user or user["password"] != form.password:
        raise HTTPException(status_code=400, detail="Error de login")
    return {"access_token": create_token({"sub": user["username"]}), "token_type": "bearer"}

@app.put("/v1/usuarios/", tags=['HTTP CRUD'])
async def update(id: int, user=Depends(check_token)): 
    return {"mensaje": "Actualizado"}

@app.delete("/v1/usuarios/", tags=['HTTP CRUD'])
async def delete(id: int, user=Depends(check_token)):
    return {"mensaje": "Eliminado"}