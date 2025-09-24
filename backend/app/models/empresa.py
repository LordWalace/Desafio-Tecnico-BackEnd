from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..db.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    cnpj = Column(String, unique=True, index=True, nullable=False)
    cidade = Column(String, index=True, nullable=False)
    ramo_atuacao = Column(String, index=True, nullable=False)
    telefone = Column(String, nullable=False)
    email_contato = Column(String, unique=True, index=True, nullable=False)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())