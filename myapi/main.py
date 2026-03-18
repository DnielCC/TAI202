
from fastapi import FastAPI
from myapi.router import usuario, misc


app = FastAPI()

app.include_router(usuario.router)
app.include_router(misc.misc)





