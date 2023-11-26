from fastapi import APIRouter, status, HTTPException, Response, Depends
from ..dependencies.oauth2 import get_current_active_integrante
from schemas.integrante import IntegranteModel
from models.integrante import integrantes
from models.tipos_integrante import tipos_integrante
from sql.database import conn
from schemas.tipo_integrante import TipoIntegrante, UpdatableColumns
from .integrante import check_for_admin_permission
from ..validators.tipos_integrante_data import validate

tipos_integrante_router = APIRouter(prefix='/api')

@tipos_integrante_router.get('/tipo-integrante/{option}')
def get_tipo_integrante(option: str = 'me', id: int | None = None, current_integrante: IntegranteModel = Depends(get_current_active_integrante)):
  if option == 'me':
    return {"id_integrante": current_integrante.id_integrante, "tipo_integrante": current_integrante.tipo}
  
  if current_integrante.tipo != 'ADM':
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'You have no permission')
  
  if option == 'id' and not (id is None):
    integrante = conn.execute(integrantes.select().where(integrantes.c.id_integrante == id)).first()
    
    if integrante:
      return {"id_integrante": id, "tipo_integrante": integrante._mapping['tipo']}

    raise HTTPException(status.HTTP_404_NOT_FOUND, 'Not such integrante')
  
  if option == 'all':
    results =  conn.execute(integrantes.select()).fetchall()
    tipos = []
    
    for result in results:
      tipos.append({"id_integrante": result._mapping['id_integrante'], 
                    "tipo_integrante": result._mapping['tipo']
                    })
    
    return {"results": tipos}
    

  raise HTTPException(status.HTTP_400_BAD_REQUEST, 'No valid option specificated')    

@tipos_integrante_router.post('/tipo-integrante')
def create_tipo_integrante(tipo_integrante: TipoIntegrante, current_integrante: IntegranteModel = Depends(check_for_admin_permission)):

  if not validate(tipo_integrante.clave_tipo, 'clave_tipo'):
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'No valid clave_tipo')

  if not validate(tipo_integrante.nombre_tipo, 'nombre_tipo'):
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'No valid nombre_tipo')
  
  try:
    conn.execute(tipos_integrante.insert().values(dict(tipo_integrante)))
    conn.commit()
  except:
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'Duplicated entry')
      
  new_tipo = conn.execute(tipos_integrante.select().where(tipos_integrante.c.clave_tipo == tipo_integrante.clave_tipo)).first()



  return Response(f'Tipo_Integrante created: {new_tipo._mapping}', status_code=status.HTTP_201_CREATED)
  
  
@tipos_integrante_router.put('/tipo-integrante')
def update_tipo_integrante(tipo_integrante: TipoIntegrante, current_integrante: IntegranteModel = Depends(check_for_admin_permission)):
  tipo_indb = conn.execute(tipos_integrante.select().where(tipos_integrante.c.clave_tipo == tipo_integrante.clave_tipo)).first()
  
  if not tipo_indb:
    raise HTTPException(status.HTTP_404_NOT_FOUND, 'No such Tipo_Integrante')
  
  changes: list[str] = []
  tipo_dict = dict(tipo_integrante)
  
  print(f'Tipo ingresado {tipo_dict}')
  print(f'Tipo in db {tipo_indb._mapping}')
  
  for column in UpdatableColumns.__args__:
    if tipo_dict[column] != tipo_indb._mapping[column]:
      changes.append(column)
  
  if not len(changes):
    return Response('No changes done', status.HTTP_200_OK)
  
  conn.execute(tipos_integrante.update().where(tipos_integrante.c.clave_tipo == tipo_integrante.clave_tipo).values(**{column: tipo_dict[column] for column in changes}))
  conn.commit()
  
  return Response('Tipo_Integrante updated', status.HTTP_200_OK)
  
    

@tipos_integrante_router.delete('/tipo-integrante')
def delete_tipo_integrante(clave_tipo:str | None = None, current_integrante: IntegranteModel = Depends(check_for_admin_permission)):
  if clave_tipo is None:
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'No clave_tipo provided')

  tipo_db = conn.execute(tipos_integrante.select().where(tipos_integrante.c.clave_tipo == clave_tipo)).first()

  if not tipo_db:
    raise HTTPException(status.HTTP_404_NOT_FOUND, 'No Tipo_Integrante with such clave_tipo')
  
  conn.execute(tipos_integrante.delete().where(tipos_integrante.c.clave_tipo == clave_tipo))
  conn.commit()

  return Response(f'Tipo_Integrante was successfully deleted {tipo_db._mapping}')