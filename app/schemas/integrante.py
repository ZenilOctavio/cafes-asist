from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class IntegranteModel(BaseModel):
  tipo:str
  nombres:str
  apellidos:str
  email:str
  telefono:str
  contrasena:str
  