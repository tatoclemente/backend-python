from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import users, auth, usersdb

app = FastAPI()

# Routers

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(usersdb.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Hola mundo"""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    """Test devuelve el id y el query param"""
    return {"item_id": item_id, "q": q}
