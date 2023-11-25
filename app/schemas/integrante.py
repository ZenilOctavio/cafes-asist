from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class CreatingIntegranteModel(BaseModel):
  tipo:str
  nombres:str
  apellidos:str
  email:str
  telefono:str
  contrasena:str
  
class UpdatingIntegranteModel(CreatingIntegranteModel):
  id_integrante: int

class IntegranteModel(UpdatingIntegranteModel):
  fecha_registro: datetime
  activo: bool


UpdatableColumns = Literal["email", "nombres", "apellidos", "telefono", "contrasena"]  