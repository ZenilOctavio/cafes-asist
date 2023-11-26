from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String,DateTime
from sql.database import meta, engine
from typing import Literal

tipo_registro = Literal['Entrada', 'Salida']

registros = Table('Registros', meta, 
                    Column('id_registro', Integer, primary_key=True),
                    Column('id_integrante', Integer, nullable=False),
                    Column('tipo_registro', String(7), nullable=False),
                    Column('fecha_hora', DateTime, nullable=False)
              )

meta.create_all(engine)