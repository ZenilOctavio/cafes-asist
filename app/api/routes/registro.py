from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..dependencies.oauth2 import get_current_active_integrante
from schemas.integrante import IntegranteModel
from schemas.registro import CreatingRegistroModel
from .integrante import check_for_admin_permission
from models.registro import registros
from sql.database import conn
from sqlalchemy import func, and_, select, insert, Select, delete
from random import randint
from datetime import datetime



registro_router = APIRouter(prefix='/api')

@registro_router.get('/registro/{option}')
def get_registro(option: str = 'me', id: int = None, starting_date: str | None = None, ending_date: str = datetime.now().date().strftime('%Y-%m-%d'), current_integrante: IntegranteModel = Depends(get_current_active_integrante)):
  if (option == 'all' or (option == 'one' or not(id is None))) and current_integrante.tipo != 'ADM':
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'You have no permission')
  
  id_integrante: int = None
  stmt: Select
  where_clauses = [func.DATE(registros.c.fecha_hora) <= ending_date]
  
  if option == 'me':
    id_integrante = current_integrante.id_integrante
  elif option == 'one':
    if id is None:
      raise HTTPException(status.HTTP_400_BAD_REQUEST, 'No id specificated')
    id_integrante = id
    
  if starting_date:
    where_clauses.append(func.DATE(registros.c.fecha_registro) >= starting_date)
  
  if (not (id_integrante is None)):
    if option is None:
      raise HTTPException(status.HTTP_400_BAD_REQUEST, 'No option specificated')

    where_clauses.append(registros.c.id_integrante == id_integrante) 
  
  
  stmt = (
    select(registros)
    .where(
      and_(*where_clauses)
    )
  )
  
  print(f'Statement: {stmt}')
    
  rows = conn.execute(stmt).fetchall()

  results = []
  
  for row in rows:
    results.append(dict(row._mapping))
  
  
  return {"results": results}
    

@registro_router.post('/registro')
def create_registro(registro_data: CreatingRegistroModel ,current_integrante: IntegranteModel = Depends(get_current_active_integrante)):
  id_integrante: int
  tipo: str
  
  if not registro_data.id_integrante is None:
    
    if current_integrante.tipo != 'ADM':
      raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'You have no permission')
    
    id_integrante = registro_data.id_integrante

  else:
    id_integrante = current_integrante.id_integrante

  date_to_search = registro_data.fecha_hora.date()
  print(f'Date to search: {date_to_search}')
  
  select_stmt = (
    select(registros)
    .where(
      and_(
        func.DATE(registros.c.fecha_hora) == date_to_search,
        registros.c.id_integrante == id_integrante
      )
    )
  )
  print(f'Statement executed: {select_stmt}')

  registro_entrada = conn.execute(select_stmt).fetchall()
  print(registro_entrada)
  
  if len((registro_entrada)) == 1:
    tipo = 'Salida'
  elif len(registro_entrada)  == 0:
    tipo = 'Entrada'
  else:
    raise HTTPException(status.HTTP_403_FORBIDDEN, 'You have already done your registros')
  
  new_registro = {
    "id_registro": randint(0,2_000_000),
    "id_integrante": id_integrante,
    "tipo_registro": tipo,
    "fecha_hora": registro_data.fecha_hora
  }
  
  insert_stmt = (
    insert(registros)
    .values(new_registro)
  )
  
  conn.execute(insert_stmt)
  conn.commit()
  
  return Response(f'Registro inserted correctly {new_registro}', status.HTTP_200_OK)
    
@registro_router.delete('/registro/{id_registro}')
def delete_registro(id_registro: int, current_integrante: IntegranteModel = Depends(check_for_admin_permission)):
  stmt = (
    delete(registros)
    .where(registros.c.id_registro == id_registro)
  )
  
  conn.execute(stmt)
  conn.commit()
  
  return Response('Deleting successfully', status.HTTP_200_OK)
