from models.integrante import integrantes
from schemas.integrante import IntegranteModel
from .database import conn
from sqlalchemy import select

def find_first_integrante(id: int) -> IntegranteModel | None:
  result = conn.execute(select(integrantes).where(integrantes.c.id_integrante == id)).first()
  
  if not result:
    return None
  
  integrante_dict = dict(result._mapping)
  
  return IntegranteModel(**integrante_dict)
  