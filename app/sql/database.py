from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = os.environ.get('DB_PORT')
DB_HOST = os.environ.get('DB_HOST')



SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
print(f'SQLAlchemy connection url: {SQLALCHEMY_DATABASE_URL}')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

meta = MetaData()

conn = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 