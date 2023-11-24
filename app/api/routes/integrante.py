from fastapi import APIRouter, status, Response
from models.integrante import integrantes
from sql.database import conn
from schemas.integrante import IntegranteModel
from hashlib import sha256
from ..validators.integrante_data import validate_email, validate_names, validate_phone
from uuid import uuid4
from datetime import datetime

integrante_router = APIRouter(prefix="/api")

@integrante_router.post('/integrante/create')
def create_integrante(integrante: IntegranteModel):
  
  if not validate_email(integrante.email):
    return Response('Not valid email', status_code=status.HTTP_406_NOT_ACCEPTABLE)

  if not validate_names(integrante.nombres):
    return Response('Not valid names', status_code=status.HTTP_406_NOT_ACCEPTABLE)

  if not validate_names(integrante.apellidos):
    return Response('Not valid lastnames', status_code=status.HTTP_406_NOT_ACCEPTABLE)

  if not validate_phone(integrante.telefono):
    return Response('Not valid phone', status_code=status.HTTP_406_NOT_ACCEPTABLE)
  
  nuevo_integrante = {
    "tipo": integrante.tipo,
    "nombres": integrante.nombres,
    "apellidos": integrante.apellidos,
    "email": integrante.email,
    "telefono": integrante.telefono,
  }
  
  nuevo_integrante["id_integrante"] = (uuid4().int >> 96) - 1
  nuevo_integrante["contrasena"] = sha256(integrante.contrasena.encode()).hexdigest()
  nuevo_integrante["activo"] = True
  nuevo_integrante["fecha_registro"] = str(datetime.utcnow())
  
  print(nuevo_integrante)
  
  result = conn.execute(integrantes.insert().values(nuevo_integrante))  
  conn.commit()
  
  return Response(f'Integrante created: {result.lastrowid}', status_code=status.HTTP_201_CREATED)