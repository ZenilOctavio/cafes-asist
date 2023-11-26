from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from sql.database import engine
from api.routes.integrante import integrante_router
from api.routes.session import session_router
from api.routes.tipos_integrante import tipos_integrante_router

engine.connect()

app = FastAPI()
app.include_router(integrante_router)
app.include_router(session_router)
app.include_router(tipos_integrante_router)

@app.get('/')
def root():
  
  return 'Hello world'