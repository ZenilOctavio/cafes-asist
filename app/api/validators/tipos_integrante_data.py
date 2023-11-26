from schemas.tipo_integrante import ValidationColumns
import re

validation_re: dict[ValidationColumns, str] = {
  'clave_tipo': r'^[A-Z]{3}$',
  'nombre_tipo': r'^[A-Za-z ]{1,100}$'
}


def validate(value: str, property: ValidationColumns ) -> bool:
  regex = re.compile(validation_re[property])
  
  if regex.fullmatch(value):
    return True
  
  return False