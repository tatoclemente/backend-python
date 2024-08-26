
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Entidad User

class User(BaseModel):
  id: int
  name: str
  surname: str
  web_site: str
  age: int

users_list = [
  User(id=1, name="John", surname="Doe", web_site="https://johndoe.com", age=24),
  User(id=2, name="Jeff", surname="Stang", web_site="https://jeff.dev", age=28),
  User(id=3, name="Alice", surname="Smith", web_site="https://alicesmith.io", age=32),
  User(id=4, name="Bob", surname="Johnson", web_site="https://bobesponja.com", age=40),
  User(id=5, name="Emily", surname="Williams", web_site="emilyrose.ar", age=28)
]

@app.get("/users-json")
async def users_json():
    return [
        { "id": 1, "name": "John", "surname": "Doe", "web_site": "https://johndoe.com", "age": 24 },
        { "id": 2, "name": "Jeff", "surname": "Stang", "web_site": "https://jeff.dev", "age": 28 },
        { "id": 3, "name": "Alice", "surname": "Smith", "web_site": "https://alicesmith.io", "age": 32 },
        { "id": 4, "name": "Bob", "surname": "Johnson", "web_site": "https://bobesponja.com", "age": 40 },
        { "id": 5, "name": "Emily", "surname": "Williams", "web_site": "emilyrose.ar", "age": 28 }
    ]
    
@app.get("/usersclass")
async def users_class():
    return users_list
  
@app.get("/user/{id}")
async def user(id: int):
  users = filter(lambda user: user.id == id, users_list)
  try:
    return list(users)[0]
  except:
    return {"error": "No se ha encontrado el usuario"}
  
@app.get("/userquery")
async def user(id: int):
  users = filter(lambda user: user.id == id, users_list)
  try:
    return list(users)[0]
  except:
    return {"error": "No se ha encontrado el usuario"}