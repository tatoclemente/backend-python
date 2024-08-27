from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str | None = None

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
    "password": "$2a$12$5dP53O8hXRoOEd.EC7qPS.cqMRATui9FWh.OqRJN7efO1U7UlpYRW"
  },
  "jane_doe": {
    "username": "jane_doe",
    "full_name": "Jane Doe",
    "email": "janedoe@mail.com",
    "disabled": True,
    "password": "$2a$12$UyWfVGYGouJKAuUvPF1pXe2CDPziS4PWM2ocbPIJgWmCgW2VzEER6",
  },
}

def search_user(username: str):
  print("USERNAME: ", username)
  if username in users_db:
    return User(**users_db[username])
  
def search_user_db(username: str):
  if username in users_db:
    return UserDB(**users_db[username])
  
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def current_user(token: Annotated[str, Depends(oauth2_scheme)]):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if not username:
      print("NO USERNAME")
      raise credentials_exception
    
    user = search_user(username)
    
    if user.disabled:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Inactive user",
      )
    return user
  except Exception as e:
    raise e
  

def verify_password(plain_password, hashed_password):
  isVerify = crypt.verify(plain_password, hashed_password)
  if not isVerify: return False
  return isVerify
  
def authenticate_user(username: str, password: str):
  user = search_user_db(username)
  print("USER: ", user)
  if not user:
      return False
  if not verify_password(password, user.password):
      return False
  return user

@router.post("/login")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
  user = authenticate_user(form.username, form.password)
  if not user:
   raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
  
  return Token(access_token = access_token, token_type = "Bearer")

@router.get("/users/me")
async def me(user: Annotated[User, Depends(current_user)]):
  return user