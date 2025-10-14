## Diferencial

# Importa as ferramentas necessárias do SQLAlchemy para definir as colunas da tabela.
from sqlalchemy import Column, Integer, String

# Importa a classe 'Base' do nosso módulo de configuração da base de dados.
# Todas as nossas classes de modelo devem herdar desta classe Base para que o SQLAlchemy as reconheça.
from ..db.database import Base


# --- Definição do Modelo 'Administrador' ---
# Esta classe representa a tabela 'administradores' na nossa base de dados.
# O SQLAlchemy ORM (Object-Relational Mapper) irá "mapear" os objetos desta classe
# para as linhas da tabela na base de dados.
class Administrador(Base):
    # O atributo __tablename__ diz ao SQLAlchemy qual o nome exato da tabela
    # que esta classe representa na base de dados.
    __tablename__ = "administradores"

    # --- Definição das Colunas da Tabela ---

    # A coluna 'id' será a chave primária da tabela.
    # - Integer: O tipo de dado é um número inteiro.
    # - primary_key=True: Define esta coluna como a chave primária, que identifica unicamente cada linha.
    # - index=True: Cria um índice para esta coluna, o que acelera as pesquisas por ID.
    id = Column(Integer, primary_key=True, index=True)

    # A coluna 'username' irá guardar o nome de utilizador do administrador.
    # - String: O tipo de dado é texto.
    # - unique=True: Garante que não podem existir dois administradores com o mesmo username.
    # - index=True: Cria um índice para acelerar as pesquisas por username (muito útil no login).
    # - nullable=False: Este campo não pode ser nulo; é obrigatório.
    username = Column(String, unique=True, index=True, nullable=False)

    # A coluna 'hashed_password' irá guardar a senha do utilizador, mas de forma segura.
    # - String: O tipo de dado é texto.
    # - nullable=False: É obrigatório que um administrador tenha uma senha.
    # IMPORTANTE: Nunca guardamos a senha original, mas sim uma versão "hash" dela.
    hashed_password = Column(String, nullable=False)