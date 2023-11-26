from pydantic import BaseModel
from typing import Literal

class TipoIntegrante(BaseModel):
  clave_tipo: str
  nombre_tipo: str
  num_horas: int
  
Columns = Literal['clave_tipo', 'nombre_tipo']