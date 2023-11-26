from fastapi import APIRouter, status, Response, Depends, HTTPException
from models.integrante import integrantes
from sql.database import conn
from schemas.integrante import IntegranteModel, CreatingIntegranteModel, UpdatingIntegranteModel, UpdatableColumns
from hashlib import sha256
from ..validators.integrante_data import validate
from datetime import datetime
from ..dependencies.oauth2 import get_current_active_integrante
from random import randint

integrante_router = APIRouter(prefix="/api")

def check_for_admin_permission(current_integrante: IntegranteModel = Depends(get_current_active_integrante)) -> IntegranteModel:
  if current_integrante.tipo != 'ADM':
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'You have no permissions')
  
  return current_integrante
  

@integrante_router.post('/integrante')
def create_integrante(integrante: CreatingIntegranteModel, current_integrante: IntegranteModel = Depends(check_for_admin_permission)):
  
  if not validate(integrante.email, 'email'):
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,'Not valid email')

  if not validate(integrante.nombres, 'nombres'):
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,'Not valid names')

  if not validate(integrante.apellidos, 'nombres'):
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,'Not valid lastnames')

  if not validate(integrante.telefono, 'telefono'):
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,'Not valid phone')

  if not validate(integrante.contrasena, 'contrasena'):
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,'Not valid password')
  
  nuevo_integrante = {
    "tipo": integrante.tipo,
    "nombres": integrante.nombres,
    "apellidos": integrante.apellidos,
    "email": integrante.email,
    "telefono": integrante.telefono,
  }
  
  nuevo_integrante["id_integrante"] = randint(0,2000000)
  nuevo_integrante["contrasena"] = sha256(integrante.contrasena.encode()).hexdigest()
  nuevo_integrante["activo"] = True
  nuevo_integrante["fecha_registro"] = str(datetime.utcnow())
  
  print(nuevo_integrante)
  
  result = conn.execute(integrantes.insert().values(nuevo_integrante))  
  conn.commit()
  
  return Response(f'Integrante created: {result.lastrowid}', status_code=status.HTTP_201_CREATED)

@integrante_router.put('/integrante')
def update_integrante(integrante: UpdatingIntegranteModel, current_integrante: IntegranteModel = Depends(check_for_admin_permission)):
  id_integrante = integrante.id_integrante
  
  integrante_db = conn.execute(integrantes.select().where(integrantes.c.id_integrante == id_integrante)).first()
  if not integrante_db:
    raise HTTPException(status.HTTP_404_NOT_FOUND, 'No such Integrante')

  changes: list[str] = [] 
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

@integrante_router.get('/integrante/{option}')
def get_integrante(id: int | None = None, option: str = 'me', current_integrante: IntegranteModel = Depends(get_current_active_integrante)):
  
  if option == 'me' or id == current_integrante.id_integrante:
    return {key: value for key, value in dict(current_integrante).items() if key != 'contrasena'}
   
  if current_integrante.tipo != 'ADM':
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'You have no permission')  
  
  if option == 'all':
    return conn.execute(integrantes.select()).fetchall()
  
  if id is None and option == 'id':
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'No id or option provided')
  
  integrante = conn.execute(integrantes.select().where(integrantes.c.id_integrante == id)).first()

  if not integrante:
    raise HTTPException(status.HTTP_404_NOT_FOUND, 'No integrante with such id')

  integrante_response = {key: value for key, value in integrante._mapping.items() if key != 'contrasena'}
  
  return integrante_response


@integrante_router.delete('/integrante')
def delete_integrante(id: int = None, current_integrante: IntegranteModel = Depends(check_for_admin_permission)):
  if id == None:
    return Response('', status.HTTP_406_NOT_ACCEPTABLE)

  integrante = conn.execute(integrantes.select().where(integrantes.c.id_integrante == id)).first()

  if not integrante:
    return Response('No Integrante with such id', status.HTTP_404_NOT_FOUND)
  
  changes = conn.execute(integrantes.update().where(integrantes.c.id_integrante == id).values(activo=False)).last_updated_params()

  return changes