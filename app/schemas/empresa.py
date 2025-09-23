from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class EmpresaBase(BaseModel):
    nome: str = Field(..., min_length=1, example="Ecomp Jr.")
    cidade: str = Field(..., min_length=1, example="Feira de Santana")
    ramo_atuacao: str = Field(..., min_length=1, example="Tecnologia")
    telefone: str = Field(..., example="(75) 99999-9999")
    
class EmpresaCreate(EmpresaBase):
    cnpj: str = Field(..., min_length=14, max_length=14, example="12345678900195")
    email_contato: EmailStr = Field(..., example="contato@ecompjr.com.br")

class EmpresaUpdate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: int
    cnpj: str
    email_contato: EmailStr
    data_cadastro: datetime

    class Config:
        orm_mode = True