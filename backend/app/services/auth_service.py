# --- Importações de Módulos ---
import os
from datetime import datetime, timedelta, timezone
# CryptContext é a ferramenta principal do passlib para gerir múltiplos algoritmos de hash.
from passlib.context import CryptContext
# JWTError para tratamento de erros e 'jwt' para criar e verificar tokens.
from jose import JWTError, jwt
# load_dotenv para carregar variáveis de ambiente a partir de um ficheiro .env.
from dotenv import load_dotenv

# --- Carregamento das Variáveis de Ambiente ---
# Carrega as variáveis definidas no ficheiro .env para o ambiente do sistema.
load_dotenv()

# --- Configurações de Segurança ---
# Lê as configurações de segurança a partir das variáveis de ambiente.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256") # Usa "HS256" como valor padrão se não for encontrado.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) # Usa 30 minutos como padrão.

# Verificação de Segurança: Garante que a aplicação não inicie sem a SECRET_KEY.
if SECRET_KEY is None:
    raise ValueError("A variável de ambiente SECRET_KEY não foi definida. Verifique o seu ficheiro .env")

# --- Configuração do Hashing de Senhas ---
# Cria um 'CryptContext' que especifica que o algoritmo de hashing a ser usado é o 'bcrypt'.
# 'deprecated="auto"' permite que o passlib atualize automaticamente os hashes se um esquema mais seguro for adicionado no futuro.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Funções de Hashing e Verificação ---

def verify_password(plain_password, hashed_password):
    """
    Verifica se uma senha em texto plano corresponde a uma senha já encriptada (hash).
    """
    # Trunca a senha em texto plano para 72 bytes antes de a verificar.
    # Isto é necessário para corresponder à forma como a senha foi guardada,
    # respeitando a limitação do bcrypt.
    return pwd_context.verify(plain_password[:72], hashed_password)

def get_password_hash(password):
    """
    Gera um hash seguro para uma senha em texto plano.
    """
    # Trunca a senha para 72 bytes para cumprir a limitação do algoritmo bcrypt.
    # Apenas os primeiros 72 bytes são usados para gerar o hash.
    return pwd_context.hash(password[:72])


# --- Funções de Token JWT ---

def create_access_token(data: dict):
    """
    Cria um novo token de acesso JWT (JSON Web Token).
    """
    # Cria uma cópia dos dados a serem codificados no token (para não modificar o dicionário original).
    to_encode = data.copy()
    
    # Define o tempo de expiração do token.
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adiciona a data de expiração ('exp') ao payload do token.
    to_encode.update({"exp": expire})
    
    # Codifica o payload usando a chave secreta e o algoritmo definidos.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Retorna o token JWT como uma string.
    return encoded_jwt