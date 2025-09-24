import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env para o ambiente
load_dotenv()

# Obtém a URL da base de dados a partir da variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

# Verifica se a variável de ambiente foi carregada corretamente
if DATABASE_URL is None:
    raise ValueError("A variável de ambiente DATABASE_URL não foi definida. Crie um ficheiro .env.")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()