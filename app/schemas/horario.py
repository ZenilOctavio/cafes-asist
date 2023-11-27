from typing import Literal
from pydantic import BaseModel
from datetime import time

Dia = Literal['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Todos']

class CreatingHorario(BaseModel):
  id_integrante: int
  dia: Dia
  entrada: time
  salida: time

class Horario(CreatingHorario):
  id_horario: int
