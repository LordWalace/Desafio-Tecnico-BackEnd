# Importa as bibliotecas necessárias para a configuração.
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# --- Carregamento das Variáveis de Ambiente ---
# A função 'load_dotenv()' lê o ficheiro '.env' na pasta 'backend'
# e carrega as variáveis definidas nele (como a DATABASE_URL) para o ambiente do sistema.
# Isto permite-nos manter as senhas e outras informações sensíveis fora do código-fonte.
load_dotenv()

# --- Configuração da Conexão com a Base de Dados ---

# Lê a string de conexão da base de dados a partir da variável de ambiente "DATABASE_URL".
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificação de Segurança: Garante que a aplicação não inicie sem a string de conexão.
# Se a variável DATABASE_URL não for encontrada no ficheiro .env, o programa irá parar
# com uma mensagem de erro clara, a evitar problemas de conexão.
if DATABASE_URL is None:
    raise ValueError("A variável de ambiente DATABASE_URL não foi definida. Crie um ficheiro .env.")

# Cria o "motor" (engine) do SQLAlchemy. O engine é o ponto de partida para qualquer
# aplicação SQLAlchemy e gere a comunicação com a base de dados através de um "pool" de conexões.
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões ('SessionLocal'). Uma sessão é a unidade de trabalho principal
# para a comunicação com a base de dados. 'autocommit=False' e 'autoflush=False' são as
# configurações padrão recomendadas para a integração com o FastAPI.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe 'Base' declarativa. Todas as nossas classes de modelo ORM (em 'models/')
# irão herdar desta classe para que o SQLAlchemy possa mapeá-las para as tabelas na base de dados.
Base = declarative_base()


# --- Dependência para Injeção de Sessão ---
# Esta função é uma "dependência" do FastAPI. Ela será chamada em cada pedido à API
# que precisar de uma ligação à base de dados.
def get_db():
    # Cria uma nova instância de sessão a partir da nossa fábrica de sessões.
    db = SessionLocal()
    try:
        # A palavra-chave 'yield' entrega a sessão de base de dados para a rota que a pediu.
        # O código da rota é executado aqui.
        yield db
    finally:
        # O bloco 'finally' garante que este código será executado sempre,
        # mesmo que ocorra um erro durante o pedido.
        # 'db.close()' fecha a sessão, a devolver a conexão para o pool do engine.
        # Isto é crucial para evitar que as conexões à base de dados se esgotem.
        db.close()