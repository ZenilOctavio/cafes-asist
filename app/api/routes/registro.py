from fastapi import APIRouter, Depends
from dependencies.oauth2 import get_current_active_integrante
from schemas.integrante import IntegranteModel
from .integrante import check_for_admin_permission

registro_router = APIRouter(prefix='/api')

@registro_router.get('/registro/{option}')
def get_registro(option: str = 'me', current_integrante: IntegranteModel = Depends(get_current_active_integrante)):
  pass

@registro_router.post('/registro')
def create_registro(current_integrante: IntegranteModel = Depends(get_current_active_integrante)):
  pass

@registro_router.put('/registro')
def update_registro(current_integrante: IntegranteModel = Depends(check_for_admin_permission)):
  pass

@registro_router.delete('/registro')
def delete_registro(current_integrante: IntegranteModel = Depends(check_for_admin_permission)):
  pass
