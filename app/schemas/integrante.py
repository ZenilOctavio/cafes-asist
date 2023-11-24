from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Integrante(BaseModel):
  id_integrante: Optional[int]
  tipo:str
  nombres:str
  apellidos:str
  email:str
  telefono:str
  contrasena:str
  activo:bool
  fecha_registro:datetime
  