import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env para o ambiente
load_dotenv()

# LÊ A SECRET_KEY E OUTRAS CONFIGURAÇÕES DO AMBIENTE
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256") # Usa "HS256" como valor padrão se não for encontrado
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) # Usa 30 como padrão

# VERIFICAÇÃO DE SEGURANÇA: Garante que a SECRET_KEY foi carregada
if SECRET_KEY is None:
    raise ValueError("A variável de ambiente SECRET_KEY não foi definida. Verifique o seu ficheiro .env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    # Trunca a senha da mesma forma para a verificação
    return pwd_context.verify(plain_password[:72], hashed_password)

def get_password_hash(password):
    # CORREÇÃO: Trunca a senha para 72 bytes para cumprir a limitação do bcrypt
    return pwd_context.hash(password[:72])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
