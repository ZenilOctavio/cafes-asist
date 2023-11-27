from models.tipos_integrante import tipos_integrante
from schemas.tipo_integrante import TipoIntegrante
from .database import conn
from sqlalchemy import select

def find_first_tipo_integrante(clave_tipo: str) -> TipoIntegrante | None:
  result = conn.execute(select(tipos_integrante).where(tipos_integrante.c.clave_tipo == clave_tipo)).first()
  
  if not result:
    return None
  
  tipo_integrante_dict = dict(result._mapping)
  
  return TipoIntegrante(**tipo_integrante_dict)