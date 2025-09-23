from fastapi import FastAPI
from .db.database import engine, Base
from .routers import empresas, auth

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gerenciamento de Empresas",
    description="API para gerenciar a carteira de clientes da Ecomp Jr.",
    version="1.0.0"
)

# Inclui as rotas
app.include_router(auth.router)
app.include_router(empresas.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Empresas da Ecomp Jr."}