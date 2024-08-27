from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, status

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
  username:   str
  full_name:  str
  email:      str
  disabled:   bool

class UserDB(User):
  password: str
  
users_db = {
  "tato_fullstack": {
    "username": "tato_fullstack",
    "full_name": "Gustavo Clemente",
    "email": "tato@mail.com",
    "disabled": False,
    "password": "123456"
  },
  "jane_doe": {
    "username": "jane_doe",
    "full_name": "Jane Doe",
    "email": "janedoe@mail.com",
    "disabled": True,
    "password": "123456",
  },
}

def search_user(username: str):
  if username in users_db:
    return User(**users_db[username])
  
def search_user_db(username: str):
  if username in users_db:
    return UserDB(**users_db[username])

async def current_user(token: str = Depends(oauth2_scheme)):
  user = search_user(token)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid authentication credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )
  if user.disabled:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Inactive user",
    )
  return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
  user_db = users_db.get(form.username)
  if not user_db:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
  user = search_user_db(form.username)
  if not form.password == user.password:
    raise HTTPException(status_code=400, detail="Incorrect username or password")
  return {"access_token": user.username, "token_type": "Bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
  return user