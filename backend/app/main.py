from fastapi import FastAPI
from .db.database import engine, Base
from .routers import empresas, auth

# 1. Importe o Middleware de CORS
from fastapi.middleware.cors import CORSMiddleware

# Cria as tabelas na base de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gerenciamento de Empresas",
    description="API para gerenciar a carteira de clientes da Ecomp Jr.",
    version="1.0.0"
)

# 2. Defina as origens permitidas (o endereço do seu front-end)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# 3. Adicione o middleware à sua aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# Inclui as rotas
app.include_router(auth.router)
app.include_router(empresas.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Empresas da Ecomp Jr."}
