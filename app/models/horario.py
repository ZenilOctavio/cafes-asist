from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String,Time
from sql.database import meta, engine


horarios = Table('Horarios', meta, 
                    Column('id_horario', Integer, primary_key=True),
                    Column('id_integrante', Integer, nullable=False),
                    Column('dia', String(9), nullable=False),
                    Column('entrada', Time, nullable=False),
                    Column('salida', Time, nullable=False, unique=True),
              )

meta.create_all(engine)