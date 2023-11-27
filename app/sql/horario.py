from .database import conn
from models.horario import horarios
from sqlalchemy import select, and_, insert
from schemas.horario import Horario, CreatingHorario
from random import randint

def find_horarios(id_integrante: int) -> list[Horario]:
  stmt = (
    select(horarios)
    .where(horarios.c.id_integrante == id_integrante)
  )
  
  rows = conn.execute(stmt).fetchall()
  
  if not rows:
    return []

  results: list[Horario] = []
  
  for row in rows:
    results.append(Horario(**dict(row._mapping)))
  
  return results

def find_horario(id_horario: int) -> Horario | None:
  stmt = (
    select(horarios)
    .where(horarios.c.id_horario == id_horario)
  )
  
  row = conn.execute(stmt).first()

  if not row:
    return None
  
  horario = Horario(**dict(row._mapping))

  return horario
  

def isthere_conflict_horario(new_horario: CreatingHorario) -> CreatingHorario | None:
  """It returns an Horario if there's a conflict"""
  
  same_day_stmt = (
    select(horarios)
    .where(
      and_(
        horarios.c.dia == new_horario.dia,
        horarios.c.id_integrante == new_horario.id_integrante
      )
    )
  )
  
  every_day_stmt = (
    select(horarios)
    .where(
      and_(
        horarios.c.dia == 'Todos',
        horarios.c.id_integrante == new_horario.id_integrante
      )
    )
  )
  
  
  row = conn.execute(same_day_stmt).first()
  
  if row:
    return Horario(**dict(row._mapping))

  row = conn.execute(every_day_stmt).first()
  
  if row:
    return Horario(**dict(row._mapping))
  

  return None

def save_horario(new_horario: CreatingHorario) -> Horario | None:
  id_horario = randint(0, 2_000_000)

  values = dict(new_horario)
  values['id_horario'] = id_horario

  stmt = (
    insert(horarios)
    .values(values)
  )
  
  conn.execute(stmt)
  conn.commit()
  
  return find_horario(id_horario)
  
  
  
    