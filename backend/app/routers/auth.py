# Ferramentas do FastAPI para criar rotas, gerir dependências e exceções.
from fastapi import APIRouter, Depends, HTTPException, status
# Classe especial do FastAPI para receber dados de formulário de login (username e password).
from fastapi.security import OAuth2PasswordRequestForm
# Ferramenta do SQLAlchemy para gerir a sessão com a base de dados.
from sqlalchemy.orm import Session

# Importa a nossa função 'get_db' para obter uma sessão da base de dados.
from ..db.database import get_db
# Importa o modelo 'Administrador' para interagir com a tabela de administradores.
from ..models.administrador import Administrador
# Importa os schemas Pydantic para validar os dados de entrada e formatar os de saída.
from ..schemas.administrador import AdminCreate, AdminResponse
from ..schemas.token import Token
# Importa o nosso serviço de autenticação, que contém a lógica de senhas e tokens JWT.
from ..services import auth_service


# --- Configuração do Roteador ---
# Cria uma instância de 'APIRouter'. Isto permite-nos organizar as nossas rotas de autenticação
# num ficheiro separado, mantendo o 'main.py' limpo.
router = APIRouter(
    prefix="/auth",  # Todos os endpoints neste ficheiro começarão com '/auth' (ex: /auth/register).
    tags=["Autenticação"]  # Agrupa estes endpoints sob a etiqueta "Autenticação" na documentação /docs.
)


# --- Endpoint de Registo ---
# Define uma rota para registar um novo administrador.
@router.post("/register", response_model=AdminResponse, status_code=status.HTTP_201_CREATED, summary="Regista um novo administrador")
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    # Procura na base de dados por um administrador com o mesmo username.
    db_admin = db.query(Administrador).filter(Administrador.username == admin.username).first()
    
    # Se um administrador com esse username já existir, lança um erro HTTP 400.
    if db_admin:
        raise HTTPException(status_code=400, detail="Username já registado.")
    
    # Se o username estiver disponível, cria um hash seguro da senha.
    hashed_password = auth_service.get_password_hash(admin.password)
    
    # Cria um novo objeto 'Administrador' com o username e a senha encriptada.
    new_admin = Administrador(username=admin.username, hashed_password=hashed_password)
    
    # Adiciona o novo administrador à sessão da base de dados.
    db.add(new_admin)
    # Confirma (faz o "commit") da transação, guardando o novo utilizador permanentemente.
    db.commit()
    # Atualiza o objeto 'new_admin' com os dados que a base de dados gerou (como o ID).
    db.refresh(new_admin)
    
    # Retorna os dados do novo administrador (sem a senha).
    return new_admin


# --- Endpoint de Login ---
# Define uma rota para o login, que irá devolver um token JWT.
@router.post("/login", response_model=Token, summary="Realiza o login e retorna um token JWT")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Procura na base de dados pelo administrador com o username fornecido no formulário.
    admin = db.query(Administrador).filter(Administrador.username == form_data.username).first()
    
    # Verifica se o administrador não existe OU se a senha fornecida está incorreta.
    # A função 'verify_password' compara a senha em texto simples com o hash guardado na base de dados.
    if not admin or not auth_service.verify_password(form_data.password, admin.hashed_password):
        # Se a autenticação falhar, lança um erro HTTP 401.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilizador ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"}, # Cabeçalho padrão para erros de autenticação.
        )
    
    # Se a autenticação for bem-sucedida, cria um novo token de acesso JWT.
    # O "sub" (subject) do token é o username, que identifica o utilizador.
    access_token = auth_service.create_access_token(
        data={"sub": admin.username}
    )
    
    # Retorna o token de acesso e o tipo de token.
    return {"access_token": access_token, "token_type": "bearer"}
