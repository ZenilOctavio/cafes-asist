from fastapi import APIRouter, status, HTTPException, Response, Depends
from .session import get_current_active_integrante
from schemas.integrante import IntegranteModel
from models.integrante import integrantes
from sql.database import conn

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
def create_tipo_integrante():
  pass

@tipos_integrante_router.put('/tipo-integrante')
def update_tipo_integrante():
  pass

@tipos_integrante_router.delete('/tipo-integrante')
def delete_tipo_integrante():
  pass