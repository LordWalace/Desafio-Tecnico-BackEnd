from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://USUARIO:SENHA@localhost/NOME_DO_BANCO" ## Adicionar o meu novo usuario e senha....C:\Program Files\PostgreSQL\<versão>\data\postgresql.conf

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()