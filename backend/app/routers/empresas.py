# Esse arquivo e o CRUD para o modelo da empresa.

# Ferramentas do FastAPI para criar rotas, gerir dependências, exceções e parâmetros de query.
from fastapi import APIRouter, Depends, HTTPException, status, Query
# Ferramenta do SQLAlchemy para gerir a sessão com a base de dados.
from sqlalchemy.orm import Session
# Tipos de dados do Python para anotações de tipo (type hints).
from typing import List, Optional

# Importa a nossa função 'get_db' para obter uma sessão da base de dados.
from ..db.database import get_db
# Importa o modelo 'Empresa' para interagir com a tabela de empresas.
from ..models.empresa import Empresa
# Importa os schemas Pydantic para validar os dados de entrada e formatar os de saída.
from ..schemas.empresa import EmpresaCreate, EmpresaResponse, EmpresaUpdate
# Importa a nossa dependência 'get_current_admin' para proteger as rotas.
from ..deps import get_current_admin

# --- Configuração do Roteador ---
# Cria uma instância de 'APIRouter' para organizar as rotas relacionadas a empresas.
router = APIRouter(
    prefix="/empresas",  # Todos os endpoints neste ficheiro começarão com '/empresas'.
    tags=["Empresas"],  # Agrupa estes endpoints sob a etiqueta "Empresas" na documentação /docs.
    dependencies=[Depends(get_current_admin)]  # Aplica a dependência de autenticação a TODAS as rotas deste ficheiro.
)


# --- Endpoint de Criação de Empresa ---
@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED, summary="Regista uma nova empresa")
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    """
    Regista uma nova empresa cliente na plataforma.
    - **cnpj**: Deve ser único.
    - **email_contato**: Deve ser único.
    """
    # Verifica se já existe uma empresa com o mesmo CNPJ para evitar duplicados.
    db_empresa_cnpj = db.query(Empresa).filter(Empresa.cnpj == empresa.cnpj).first()
    if db_empresa_cnpj:
        raise HTTPException(status_code=400, detail="CNPJ já registado.")
        
    # Verifica se já existe uma empresa com o mesmo email para evitar duplicados.
    db_empresa_email = db.query(Empresa).filter(Empresa.email_contato == empresa.email_contato).first()
    if db_empresa_email:
        raise HTTPException(status_code=400, detail="Email de contacto já registado.")

    # Cria uma nova instância do modelo 'Empresa' com os dados validados pelo schema.
    new_empresa = Empresa(**empresa.dict())
    # Adiciona o novo objeto à sessão da base de dados.
    db.add(new_empresa)
    # Confirma (faz o "commit") da transação, guardando a nova empresa.
    db.commit()
    # Atualiza o objeto 'new_empresa' com os dados gerados pela base de dados (ID, data_cadastro).
    db.refresh(new_empresa)
    # Retorna os dados da empresa recém-criada.
    return new_empresa


# --- Endpoint de Listagem de Empresas (com Filtros) ---
@router.get("/", response_model=List[EmpresaResponse], summary="Lista todas as empresas com filtros")
def get_empresas(
    cidade: Optional[str] = Query(None, description="Filtra empresas por cidade"),
    ramo_atuacao: Optional[str] = Query(None, description="Filtra empresas por ramo de atuação"),
    nome: Optional[str] = Query(None, description="Busca textual pelo nome da empresa"),
    db: Session = Depends(get_db)
):
    """
    Lista todas as empresas registadas com opções de filtro e busca.
    """
    # Inicia uma consulta à tabela de empresas.
    query = db.query(Empresa)
    
    # Aplica os filtros à consulta, se eles forem fornecidos no pedido.
    # '.ilike()' faz uma busca "case-insensitive" (não diferencia maiúsculas de minúsculas).
    if cidade:
        query = query.filter(Empresa.cidade.ilike(f"%{cidade}%"))
    if ramo_atuacao:
        query = query.filter(Empresa.ramo_atuacao.ilike(f"%{ramo_atuacao}%"))
    if nome:
        query = query.filter(Empresa.nome.ilike(f"%{nome}%"))
    
    # Executa a consulta e retorna todos os resultados.
    return query.all()


# --- Endpoint de Detalhe de Empresa ---
@router.get("/{empresa_id}", response_model=EmpresaResponse, summary="Detalha uma empresa por ID")
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """
    Exibe os detalhes de uma única empresa através do seu ID.
    """
    # Procura pela empresa com o ID fornecido.
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    
    # Se a empresa não for encontrada, lança um erro HTTP 404.
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    
    # Retorna os dados da empresa encontrada.
    return db_empresa


# --- Endpoint de Atualização de Empresa ---
@router.put("/{empresa_id}", response_model=EmpresaResponse, summary="Atualiza os dados de uma empresa")
def update_empresa(empresa_id: int, empresa_update: EmpresaUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de uma empresa, exceto id, cnpj e data de registo.
    """
    # Procura pela empresa que será atualizada.
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    # Converte o schema de atualização num dicionário, excluindo os campos que não foram enviados.
    update_data = empresa_update.dict(exclude_unset=True)
    
    # Itera sobre os dados enviados e atualiza os atributos correspondentes no objeto da empresa.
    for key, value in update_data.items():
        setattr(db_empresa, key, value)
    
    # Confirma (faz o "commit") das alterações na base de dados.
    db.commit()
    # Atualiza o objeto para refletir os dados guardados.
    db.refresh(db_empresa)
    
    # Retorna a empresa com os dados atualizados.
    return db_empresa


# --- Endpoint de Exclusão de Empresa ---
@router.delete("/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Exclui uma empresa")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """
    Remove uma empresa da base de dados.
    """
    # Procura pela empresa que será excluída.
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    # Remove o objeto da sessão da base de dados.
    db.delete(db_empresa)
    # Confirma (faz o "commit") da exclusão.
    db.commit()
    
    # Retorna uma resposta vazia com status 204, a indicar sucesso.
    return
