from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from sql.database import meta, engine


prueba_trabajo = Table('PruebaTrabajo', meta, 
                    Column('id_prueba', Integer, primary_key=True),
                    Column('id_registro', Integer, nullable=False),
                    Column('id_integrante', Integer, nullable=False),
                    Column('titulo', String(100), nullable=False),
                    Column('descripcion', String(200)),
                    Column('ubicacion_prueba', String(300), nullable=False),
              )

meta.create_all(engine)