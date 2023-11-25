from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from models.integrante import integrantes
from sql.database import conn
from hashlib import sha256
from schemas.integrante import IntegranteModel
from schemas.session import Token, TokenData
from fastapi import APIRouter


SECRET_KEY = "SecretKeyForHashingInMyApp"
ALGORITHM = "HS256"
EXPIRES_IN_MINUTES = 600

session_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str):
  password_hash = sha256(plain_password.encode()).hexdigest()
  
  return hashed_password == password_hash

def get_password_hash(password: str):
  return sha256(password.encode()).hexdigest()

def get_integrante(email: str) -> IntegranteModel:
  integrante = conn.execute(integrantes.select().where(integrantes.c.email == email)).first()
  
  if not integrante:
    return None

  integrante_dict = { key: value for key, value in integrante._mapping.items()}
  return IntegranteModel(**integrante_dict)
  

def authenticate_integrante(email: str, password:str):
  integrante = get_integrante(email)
  
  if not integrante:
    return None
  
  if not verify_password(password, integrante.contrasena):
    return None
  
  return integrante


def create_access_token(data: dict, expires_delta: timedelta | None):
  to_encode = data.copy()
  
  if expires_delta:
    expires = datetime.utcnow() + expires_delta
  else:
    expires = datetime.utcnow() + timedelta(minutes=50)

  to_encode.update({"exp": expires})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  
  return encoded_jwt  

async def get_current_integrante(token: str = Depends(oauth2_scheme)) -> IntegranteModel:
  credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                       detail="Could not validate credentials", 
                                       headers={"WWW-Authenticate": "Bearer"})
  
  try: 
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    
    if email is None:
      raise credential_exception
    
    token_data = TokenData(email=email)
  except JWTError:
    raise credential_exception
  
  integrante = get_integrante(token_data.email)
  
  if integrante is None:
    raise credential_exception
  
  return integrante

async def get_current_active_integrante(current_integrante: IntegranteModel = Depends(get_current_integrante)):
  if not current_integrante.activo:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive integrante")
  
  return current_integrante

@session_router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
  user = authenticate_integrante(form_data.username, form_data.password)
  
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Incorrect username or password",
                        headers={"WWW-Authenticate": "Bearer"}
                        )
    
  access_token_expires = timedelta(minutes=EXPIRES_IN_MINUTES)
  access_token = create_access_token(data={"sub": user.email},expires_delta=access_token_expires)
  
  return {"access_token": access_token, "token_type": "bearer"}

@session_router.get('/token/validate')
async def validate_token(integrante: IntegranteModel = Depends(get_current_active_integrante)):
  return integrante