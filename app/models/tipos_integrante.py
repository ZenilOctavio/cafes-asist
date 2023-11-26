from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from sql.database import meta, engine


tipos_integrante = Table('Tipos_integrante', meta, 
                    Column('clave_tipo', String(3), primary_key=True),
                    Column('nombre_tipo', String(100), nullable=False),
                    Column('num_horas', Integer, nullable=False)
              )

meta.create_all(engine)