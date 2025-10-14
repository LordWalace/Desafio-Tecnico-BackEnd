# Importa ferramentas do Pydantic para criar modelos de dados e validar tipos específicos,
# como 'EmailStr' para emails e 'Field' para validações avançadas (ex: comprimento mínimo).
from pydantic import BaseModel, EmailStr, Field
# Importa o tipo 'datetime' para trabalhar com datas e horas.
from datetime import datetime


# --- Schema Base da Empresa ---
# Esta classe 'EmpresaBase' serve como um modelo fundamental que contém os campos comuns
# a todas as outras variações de schemas de empresa (criação, atualização, resposta).
# Isto evita a repetição de código, seguindo o princípio DRY (Don't Repeat Yourself).
class EmpresaBase(BaseModel):
    # Field(..., min_length=1) define que o campo é obrigatório e deve ter pelo menos 1 caractere.
    # 'example' é usado para gerar exemplos na documentação da API em /docs.
    nome: str = Field(..., min_length=1, example="Ecomp Jr.")
    cidade: str = Field(..., min_length=1, example="Feira de Santana")
    ramo_atuacao: str = Field(..., min_length=1, example="Tecnologia")
    telefone: str = Field(..., example="(75) 99999-9999")
    

# --- Schema para a Criação de uma Empresa ---
# Herda de 'EmpresaBase' e adiciona os campos específicos necessários apenas na criação.
class EmpresaCreate(EmpresaBase):
    # Adiciona validações para o CNPJ, garantindo que ele tenha exatamente 14 caracteres.
    cnpj: str = Field(..., min_length=14, max_length=14, example="12345678000195")
    
    # Usa o tipo 'EmailStr' do Pydantic para validar automaticamente se o valor é um email válido.
    email_contato: EmailStr = Field(..., example="contato@ecompjr.com.br")


# --- Schema para a Atualização de uma Empresa ---
# Herda de 'EmpresaBase'. Campos como 'cnpj' e 'email_contato' não estão aqui
# porque os requisitos podem especificar que eles não são editáveis.
# A palavra-chave 'pass' indica que esta classe não adiciona nenhum novo campo,
# mas herda todos os campos de 'EmpresaBase'.
class EmpresaUpdate(EmpresaBase):
    pass


# --- Schema para a Resposta da API ---
# Define a estrutura dos dados de uma empresa que serão enviados de volta ao cliente.
# Herda de 'EmpresaBase' e adiciona os campos gerados pela base de dados.
class EmpresaResponse(EmpresaBase):
    # 'id' é gerado pela base de dados, por isso só aparece na resposta.
    id: int
    
    # Inclui 'cnpj' e 'email_contato' na resposta.
    cnpj: str
    email_contato: EmailStr
    
    # 'data_cadastro' também é gerado pela base de dados.
    data_cadastro: datetime

    # --- Configuração do Schema ---
    # A classe interna 'Config' permite-nos ajustar o comportamento do Pydantic.
    class Config:
        # 'orm_mode = True' (ou 'from_attributes = True' em versões mais recentes)
        # permite ao Pydantic ler os dados diretamente de um objeto do SQLAlchemy,
        # facilitando a conversão do modelo da base de dados para a resposta da API.
        orm_mode = True