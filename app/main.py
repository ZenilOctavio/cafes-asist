from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from sql.database import engine
from api.routes.integrante import integrante_router

engine.connect()

app = FastAPI()
app.include_router(integrante_router)

@app.get('/')
def root():
  
  return 'Hello world'