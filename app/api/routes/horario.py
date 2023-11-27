from fastapi import APIRouter, Depends, HTTPException, status, Response
from .integrante import check_for_admin_permission
from ..dependencies.oauth2 import get_current_active_integrante
from schemas.integrante import IntegranteModel
from sql.database import conn
from sql.integrante import find_first_integrante
from sql.tipo_integrante import find_first_tipo_integrante
from sql.horario import isthere_conflict_horario, save_horario

from models.horario import horarios
from sqlalchemy import select, Select
from schemas.horario import Dia, CreatingHorario
from datetime import datetime, time

horario_router = APIRouter(prefix='/api')

@horario_router.get('/horario')
def get_horario(option:str = 'me', current_integrante: IntegranteModel = Depends(get_current_active_integrante)):

  stmt: Select
  
  if option == 'me':
    stmt = (
      select(horarios)
      .where(horarios.c.id_integrante == current_integrante.id_integrante)
    )
  elif option == 'all':
    if current_integrante.tipo != 'ADM':
      raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'You have no permission')
    
    stmt = (select(horarios))
  
  rows = conn.execute(stmt).fetchall()
  
  results = []
  
  for row in rows:
    results.append(dict(row._mapping))
  
  return {"results": results}


@horario_router.post('/horario')
def post_horario(horario_data: CreatingHorario, current_integrante = Depends(check_for_admin_permission)):
  integrante = find_first_integrante(horario_data.id_integrante)
  
  if not integrante:
    raise HTTPException(status.HTTP_404_NOT_FOUND, 'No Integrante with such id')
  
  tipo_integrante = find_first_tipo_integrante(integrante.tipo)
  
  
  print(f'Entrada {horario_data.entrada} - Salida {horario_data.salida}')
  common_date = datetime(2023,8,21)

  start_date = datetime.combine(common_date, horario_data.entrada)
  end_date = datetime.combine(common_date, horario_data.salida)

  difference_hours = ((end_date - start_date).total_seconds()) / 3600
  
  if difference_hours != float(tipo_integrante.num_horas):
    raise HTTPException(status.HTTP_403_FORBIDDEN, f'entrada and salida doesn\'t achieve the number of expected hours {difference_hours} -> {tipo_integrante.num_horas}')
  
  conflict_horario = isthere_conflict_horario(horario_data)
  
  if conflict_horario:
    raise HTTPException(status.HTTP_403_FORBIDDEN, f'There\'s already an Horario for that day -> Entrada: {conflict_horario.entrada} | Salida: {conflict_horario.salida}')
  
  new_horario = save_horario(horario_data)
  
  return {"new_horario": new_horario}

@horario_router.put('/horario')
def put_horario():
  pass

@horario_router.delete('/horario')
def delete_horario():
  pass