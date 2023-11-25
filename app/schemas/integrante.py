from pydantic import BaseModel
from typing import Literal


class IntegranteModel(BaseModel):
  tipo:str
  nombres:str
  apellidos:str
  email:str
  telefono:str
  contrasena:str
  
class UpdatingIntegranteModel(IntegranteModel):
  id_integrante: int


UpdatableColumns = Literal["email", "nombres", "apellidos", "telefono", "contrasena"]  