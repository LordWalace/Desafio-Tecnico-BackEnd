# Ferramentas do FastAPI para injeção de dependências e tratamento de exceções HTTP.
from fastapi import Depends, HTTPException, status
# A classe que define o esquema de segurança "OAuth2 com Password Flow".
from fastapi.security import OAuth2PasswordBearer
# Ferramentas da biblioteca 'jose' para descodificar e validar tokens JWT.
from jose import JWTError, jwt
# Ferramenta do SQLAlchemy para gerir a sessão com a base de dados.
from sqlalchemy.orm import Session

# Importa as nossas dependências e serviços locais.
from .db.database import get_db
from .services import auth_service
from .schemas.token import TokenData
from .models.administrador import Administrador

# --- Configuração do Esquema de Autenticação OAuth2 ---
# Cria uma instância do 'OAuth2PasswordBearer'.
# O argumento 'tokenUrl="auth/login"' informa à documentação /docs
# que o endpoint para obter o token é '/auth/login'.
# O FastAPI usará esta instância para extrair automaticamente o token do cabeçalho "Authorization" de um pedido.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Dependência de Verificação de Autenticação ---
# Esta função assíncrona é a nossa dependência de segurança principal.
# Quando a aplicamos a uma rota, o FastAPI irá executá-la antes do código da rota.
# A sua missão é: validar o token e devolver os dados do utilizador autenticado.
async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Prepara uma exceção padrão que será usada em vários cenários de falha.
    # 'status.HTTP_401_UNAUTHORIZED' é o código para "Não Autenticado".
    # O cabeçalho 'WWW-Authenticate' é parte do padrão OAuth2.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Tenta descodificar o token JWT recebido do cliente.
        # Usa a nossa SECRET_KEY e o ALGORITHM definidos no 'auth_service'.
        payload = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])
        
        # Extrai o 'username' do payload do token. Usamos a chave "sub" (subject) por convenção.
        username: str = payload.get("sub")
        
        # Se o username não for encontrado no token, ele é inválido. Lança a exceção.
        if username is None:
            raise credentials_exception
            
        # Valida se os dados do payload correspondem ao nosso schema 'TokenData'.
        token_data = TokenData(username=username)

    except JWTError:
        # Se 'jwt.decode' falhar (por exemplo, token expirado ou assinatura inválida),
        # a biblioteca 'jose' levanta um 'JWTError'. Capturamo-lo e lançamos a nossa exceção 401.
        raise credentials_exception
    
    # Se o token foi descodificado com sucesso, agora verificamos se o utilizador realmente existe na base de dados.
    admin = db.query(Administrador).filter(Administrador.username == token_data.username).first()
    
    # Se o utilizador não for encontrado na base de dados (ex: foi apagado depois da emissão do token),
    # o token já não é válido. Lança a exceção.
    if admin is None:
        raise credentials_exception
        
    # Se todas as verificações passarem, a função devolve o objeto 'admin' da base de dados.
    # A rota que usou esta dependência receberá este objeto e poderá usá-lo.
    return admin