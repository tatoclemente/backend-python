
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema

router = APIRouter(prefix="/userdb",
                   tags=["users_db"],
                   responses={ status.HTTP_404_NOT_FOUND: { "message": "No encontrado"} }
                  )

# Entidad User DB


users_list = []

@router.get("/all", response_model=list[User])
async def users_class():
    try:
        users = db_client.users.find()
        return users_schema(users)
    except ValueError:
        return {"error": "No se han encontrado usuarios"}
      
@router.get("/{id}")
async def user_by_id(id: str):
    try:
        user = search_user("_id", ObjectId(id))
        return user
    except ValueError:
        return {"error": "No se ha encontrado el usuario"}

  
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(user: User):
    try:
        user_find = search_user("email", user.email)
        if isinstance(user_find, User):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe")
      
        user_dict = user.model_dump()
        del user_dict["id"]
        
        print("USER_DICT: ", user_dict)
        
        id = db_client.users.insert_one(user_dict).inserted_id    
        user_db = db_client.users.find_one({"_id": id})
        new_user = user_schema(user_db)
        return new_user
    
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="Error al crear el usuario") from exc
  
  
    
@router.put("/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(id: str, user: User):
    print(id)
    try:
      
        # Verificar si el id es un ObjectId válido
        try:
            object_id = ObjectId(id)
        except InvalidId as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="ID de usuario no válido") from exc
            
        user_dict = user.model_dump()    
        del user_dict["id"]
        print("USER_DICT: ", user_dict)    
        found = db_client.users.find_one_and_update(
            {"_id": object_id}, {"$set": user_dict})
        
        print("FOUND: ", found)
    
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="No se ha encontrado el usuario")
        
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Error al actualizar el usuario") from exc
        
    return search_user("_id", object_id)
  
  
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)}) 
  
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No se ha encontrado el usuario")
  
  
  
def search_user(field: str, key):
    """Función genérica para buscar usuarios"""
    try:
        user_db = db_client.users.find_one({ field: key })
        if not user_db:
            return None
        return user_schema(user_db)
    except ValueError as e:
        return {"message": "Ups! Algo no anda bien", "error": e} 
