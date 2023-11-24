import re

def validate_email(email: str) -> bool:
  regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
  
  if regex.fullmatch(email):
    return True
  
  return False

def validate_names(name: str) -> bool:
  regex = re.compile(r'^[A-Za-z ]{1,50}$')

  if regex.fullmatch(name):
    return True
  
  return False

def validate_phone(phone: str) -> bool:
  regex = re.compile(r'^\d{10}$')

  if regex.fullmatch(phone):
    return True
  
  return False
  