from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime
from sql.database import meta, engine


integrantes = Table('Integrantes', meta, 
                    Column('id_integrante', Integer, primary_key=True),
                    Column('tipo', String(3), nullable=False),
                    Column('nombres', String(50), nullable=False),
                    Column('apellidos', String(100), nullable=False),
                    Column('email', String(50), nullable=False, unique=True),
                    Column('telefono', String(10), nullable=False, unique=True),
                    Column('contrasena', String(64), nullable=False),
                    Column('activo', Boolean, nullable=False),
                    Column('fecha_registro', DateTime, nullable=False)     
              )

meta.create_all(engine)