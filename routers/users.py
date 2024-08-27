
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/user", 
                   tags=["users"],
                   responses={ status.HTTP_404_NOT_FOUND: { "message": "No encontrado"} }
                  )

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

@router.get("/users-json")
async def users_json():
    return [
        { "id": 1, "name": "John", "surname": "Doe", "web_site": "https://johndoe.com", "age": 24 },
        { "id": 2, "name": "Jeff", "surname": "Stang", "web_site": "https://jeff.dev", "age": 28 },
        { "id": 3, "name": "Alice", "surname": "Smith", "web_site": "https://alicesmith.io", "age": 32 },
        { "id": 4, "name": "Bob", "surname": "Johnson", "web_site": "https://bobesponja.com", "age": 40 },
        { "id": 5, "name": "Emily", "surname": "Williams", "web_site": "emilyrose.ar", "age": 28 }
    ]
    
@router.get("/users")
async def users_class():
    return users_list
  
@router.get("/{id}")
async def user(id: int):
  users = filter(lambda user: user.id == id, users_list)
  try:
    return list(users)[0]
  except:
    return {"error": "No se ha encontrado el usuario"}
  
@router.get("/userquery")
async def user(id: int):
  users = filter(lambda user: user.id == id, users_list)
  try:
    return list(users)[0]
  except:
    return {"error": "No se ha encontrado el usuario"}
  
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(user: User):
  if type(search_user(user.id)) == User:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
  else: 
    users_list.routerend(user)
    return user
    
@router.put("/", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user: User):
  
  found = False
  
  for index, saved_user in enumerate(users_list):
    if saved_user.id == user.id:
      users_list[index] = user
      found = True
      return user
  if not found:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el usuario")
  
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int):
  found = False
  for index, saved_user in enumerate(users_list):
    if saved_user.id == id:
      del users_list[index]
      found = True
      return {"message": "Usuario eliminado"}
  if not found:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el usuario")
  
def search_user(id: int):
  users = filter(lambda user: user.id == id, users_list)
  try:
    return list(users)[0]
  except:
    return {"error": "No se ha encontrado el usuario"}