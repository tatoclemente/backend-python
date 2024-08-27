from typing import Union
from fastapi import FastAPI
from routers import users, auth
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers

app.include_router(users.router)
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
