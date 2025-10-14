# Importa as classes e funções necessárias das bibliotecas.
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# Importa os componentes locais da aplicação.
from .db.database import engine, Base
from .routers import empresas, auth

# --- Criação das Tabelas na Base de Dados ---
# Esta linha lê os modelos definidos em 'models/' e cria as tabelas correspondentes
# na base de dados PostgreSQL, caso elas ainda não existam.
# É executado apenas uma vez quando a aplicação inicia.
Base.metadata.create_all(bind=engine)

# --- Metadados para a Documentação da API ---
# Define as "tags" que serão usadas para agrupar os endpoints na documentação (/docs).
# Isto melhora a organização e a legibilidade da interface do Swagger UI.
tags_metadata = [
    {
        "name": "Autenticação",
        "description": "Operações de registo e login para obter tokens de acesso.",
    },
    {
        "name": "Empresas",
        "description": "Operações para gerir as empresas clientes (CRUD e consultas avançadas).",
    },
]

# --- Instanciação da Aplicação FastAPI ---
# Cria a instância principal da aplicação FastAPI, passando os metadados
# que serão exibidos na documentação automática.
app = FastAPI(
    title="API de Gestão de Clientes - Ecomp Jr.",
    description="API desenvolvida para o Desafio Técnico do Processo Seletivo 2025.2 da Ecomp Jr.",
    version="1.0.0",
    contact={
        "name": "Ecomp Jr. - Empresa Júnior de Computação",
        "url": "http://ecompjr.com.br/",
        "email": "ecompjr@uefs.br",
    },
    openapi_tags=tags_metadata
)

# --- Configuração do CORS (Cross-Origin Resource Sharing) ---
# O CORS permite que o nosso front-end (a correr, por exemplo, em http://localhost:5173)
# possa fazer pedidos a esta API (a correr em http://localhost:8000).
# Sem esta configuração, o navegador bloquearia os pedidos por segurança.

# Lista de origens (URLs do front-end) que têm permissão para aceder à API.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Permite as origens da lista
    allow_credentials=True,      # Permite o envio de cookies/autenticação
    allow_methods=["*"],         # Permite todos os métodos HTTP (GET, POST, PUT, etc.)
    allow_headers=["*"],         # Permite todos os cabeçalhos HTTP
)

# --- Inclusão das Rotas (Routers) ---
# Inclui os ficheiros de rotas na aplicação principal. Isto mantém o código organizado,
# separando a lógica de cada recurso (autenticação, empresas, etc.) em ficheiros diferentes.
app.include_router(auth.router)
app.include_router(empresas.router)

# --- Rota Principal (Endpoint Raiz) ---
# Define o comportamento da rota principal da API ("/").

# Obtém o caminho absoluto para o ficheiro 'docs_redirect.html'
redirect_file_path = os.path.join(os.path.dirname(__file__), "docs_redirect.html")

@app.get("/", tags=["Root"], include_in_schema=False)
def read_root():
    """
    Esta rota serve um ficheiro HTML que redireciona automaticamente o utilizador
    para a página de documentação interativa em /docs.
    Isto facilita o acesso à documentação para quem está a testar a API.
    """
    return FileResponse(redirect_file_path)