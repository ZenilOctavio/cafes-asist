from pydantic import BaseModel
from typing import Literal

class TipoIntegrante(BaseModel):
  clave_tipo: str
  nombre_tipo: str
  num_horas: int
  
ValidationColumns = Literal['clave_tipo', 'nombre_tipo']

UpdatableColumns = Literal['nombre_tipo', 'num_horas']