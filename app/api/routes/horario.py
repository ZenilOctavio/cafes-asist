from fastapi import APIRouter

horario_router = APIRouter(prefix='/api')

@horario_router.get('/horario')
def get_horario():
  pass

@horario_router.post('/horario')
def post_horario():
  pass

@horario_router.put('/horario')
def put_horario():
  pass

@horario_router.delete('/horario')
def delete_horario():
  pass