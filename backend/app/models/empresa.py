# Importa as ferramentas necessárias do SQLAlchemy para definir os tipos de dados das colunas
# e para usar funções do servidor da base de dados (como a data e hora atuais).
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

# Importa a classe 'Base' do nosso módulo de configuração da base de dados.
# Todas as nossas classes de modelo devem herdar desta classe Base.
from ..db.database import Base


# --- Definição do Modelo 'Empresa' ---
# Esta classe representa a tabela 'empresas' na nossa base de dados.
# O SQLAlchemy ORM irá mapear os objetos desta classe para as linhas da tabela.
class Empresa(Base):
    # O atributo __tablename__ define o nome exato da tabela na base de dados.
    __tablename__ = "empresas"

    # --- Definição das Colunas da Tabela ---

    # A coluna 'id' será a chave primária, um número inteiro que se auto-incrementa.
    # - Integer: O tipo de dado é um número inteiro.
    # - primary_key=True: Define esta coluna como a chave primária, que identifica unicamente cada empresa.
    # - index=True: Cria um índice para acelerar as pesquisas por ID.
    id = Column(Integer, primary_key=True, index=True)

    # A coluna 'nome' irá guardar o nome da empresa.
    # - String: O tipo de dado é texto.
    # - index=True: Cria um índice para acelerar as pesquisas por nome.
    # - nullable=False: Este campo não pode ser nulo; é obrigatório.
    nome = Column(String, index=True, nullable=False)

    # A coluna 'cnpj' irá guardar o CNPJ da empresa.
    # - String: O tipo de dado é texto.
    # - unique=True: Garante que não podem existir duas empresas com o mesmo CNPJ, conforme o requisito.
    # - index=True: Cria um índice para acelerar as pesquisas por CNPJ.
    # - nullable=False: Este campo é obrigatório.
    cnpj = Column(String, unique=True, index=True, nullable=False)

    # A coluna 'cidade' irá guardar a cidade da empresa.
    cidade = Column(String, index=True, nullable=False)

    # A coluna 'ramo_atuacao' irá guardar o ramo de atuação da empresa.
    ramo_atuacao = Column(String, index=True, nullable=False)

    # A coluna 'telefone' irá guardar o telefone de contacto da empresa.
    telefone = Column(String, nullable=False)

    # A coluna 'email_contato' irá guardar o email de contacto da empresa.
    # - unique=True: Garante que não podem existir duas empresas com o mesmo email de contacto.
    email_contato = Column(String, unique=True, index=True, nullable=False)

    # A coluna 'data_cadastro' irá guardar a data e hora em que a empresa foi registada.
    # - DateTime(timezone=True): Armazena a data e a hora com informação de fuso horário.
    # - server_default=func.now(): Define o valor padrão no lado da base de dados.
    #   Sempre que uma nova empresa for criada, a base de dados irá preencher este campo
    #   automaticamente com a data e hora atuais.
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())