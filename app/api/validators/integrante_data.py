import re
from schemas.integrante import UpdatableColumns

validation_re: dict[UpdatableColumns, str] = {
  "email": r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',
  "nombres": r'^[A-Za-z ]{1,50}$',
  "apellidos": r'^[A-Za-z ]{1,50}$',
  "telefono": r'^\d{10}$',
  "contrasena": r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
}


def validate(value: str, property: UpdatableColumns ) -> bool:
  regex = re.compile(validation_re[property])
  
  if regex.fullmatch(value):
    return True
  
  return False

