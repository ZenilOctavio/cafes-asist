from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from hashlib import sha256
from schemas.integrante import IntegranteModel
from schemas.session import Token
from fastapi import APIRouter
from ..dependencies.oauth2 import authenticate_integrante, create_access_token, get_current_active_integrante




session_router = APIRouter()



@session_router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
  user = authenticate_integrante(form_data.username, form_data.password)
  
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Incorrect username or password",
                        headers={"WWW-Authenticate": "Bearer"}
                        )
    
  access_token = create_access_token(data={"sub": user.email})
  
  return {"access_token": access_token, "token_type": "bearer"}

@session_router.get('/token/validate')
async def validate_token(integrante: IntegranteModel = Depends(get_current_active_integrante)):
  return integrante