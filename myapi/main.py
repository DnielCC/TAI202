
from fastapi import FastAPI
from myapi.router import usuario, misc
from myapi.data.db import engine
from myapi.data import usuarios as UsuarioDB

UsuarioDB.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(usuario.router)
app.include_router(misc.misc)





