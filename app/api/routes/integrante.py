from fastapi import APIRouter, status, Response
from models.integrante import integrantes
from sql.database import conn
from schemas.integrante import CreatingIntegranteModel, UpdatingIntegranteModel, UpdatableColumns
from hashlib import sha256
from ..validators.integrante_data import validate
from uuid import uuid4
from datetime import datetime

integrante_router = APIRouter(prefix="/api")

@integrante_router.post('/integrante')
def create_integrante(integrante: CreatingIntegranteModel):
  
  if not validate(integrante.email, 'email'):
    return Response('Not valid email', status_code=status.HTTP_406_NOT_ACCEPTABLE)

  if not validate(integrante.nombres, 'nombres'):
    return Response('Not valid names', status_code=status.HTTP_406_NOT_ACCEPTABLE)

  if not validate(integrante.apellidos, 'nombres'):
    return Response('Not valid lastnames', status_code=status.HTTP_406_NOT_ACCEPTABLE)

  if not validate(integrante.telefono, 'telefono'):
    return Response('Not valid phone', status_code=status.HTTP_406_NOT_ACCEPTABLE)

  if not validate(integrante.contrasena, 'contrasena'):
    return Response('Not valid password', status_code=status.HTTP_406_NOT_ACCEPTABLE)
  
  nuevo_integrante = {
    "tipo": integrante.tipo,
    "nombres": integrante.nombres,
    "apellidos": integrante.apellidos,
    "email": integrante.email,
    "telefono": integrante.telefono,
  }
  
  nuevo_integrante["id_integrante"] = ((uuid4().int >> 96) & (0xFFFFFFFF))
  nuevo_integrante["contrasena"] = sha256(integrante.contrasena.encode()).hexdigest()
  nuevo_integrante["activo"] = True
  nuevo_integrante["fecha_registro"] = str(datetime.utcnow())
  
  print(nuevo_integrante)
  
  result = conn.execute(integrantes.insert().values(nuevo_integrante))  
  conn.commit()
  
  return Response(f'Integrante created: {result.lastrowid}', status_code=status.HTTP_201_CREATED)

@integrante_router.put('/integrante')
def update_integrante(integrante: UpdatingIntegranteModel):
  id_integrante = integrante.id_integrante
  
  integrante_db = conn.execute(integrantes.select().where(integrantes.c.id_integrante == id_integrante)).first()
  changes: list[int] = [] 
  integrante_dict = dict(integrante)
  integrante_dict['contrasena'] = sha256(integrante.contrasena.encode()).hexdigest()

  changes: list[UpdatableColumns] = []
  
  for column in UpdatableColumns.__args__:
    if integrante_dict[column] != integrante_db._mapping[column]:
      changes.append(column)

  if not len(changes):
    return Response('No changes done', status.HTTP_200_OK)
  
  
  conn.execute(integrantes.update().where(integrantes.c.id_integrante == id_integrante).values(**{ change: integrante_dict[change] for change in changes }))
  conn.commit()
    
  return Response('User was updated', status.HTTP_200_OK)

@integrante_router.get('/integrante')
def get_integrante(id: int = None):
  if id == None:
    return Response('', status.HTTP_406_NOT_ACCEPTABLE)
  
  integrante = conn.execute(integrantes.select().where(integrantes.c.id_integrante == id)).first()

  if not integrante:
    return Response('No Integrante with such id', status.HTTP_404_NOT_FOUND)

  integrante_response = {key: value for key, value in integrante._mapping.items() if key != 'contrasena'}
  
  return integrante_response


@integrante_router.delete('/integrante')
def delete_integrante(id: int = None):
  if id == None:
    return Response('', status.HTTP_406_NOT_ACCEPTABLE)

  integrante = conn.execute(integrantes.select().where(integrantes.c.id_integrante == id)).first()

  if not integrante:
    return Response('No Integrante with such id', status.HTTP_404_NOT_FOUND)
  
  changes = conn.execute(integrantes.update().where(integrantes.c.id_integrante == id).values(activo=False)).last_updated_params()

  return changes