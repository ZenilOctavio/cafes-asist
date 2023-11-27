from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreatingRegistroModel(BaseModel):
  fecha_hora: datetime
  id_integrante: Optional[int]

