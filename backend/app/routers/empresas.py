from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.database import get_db
from ..models.empresa import Empresa
from ..schemas.empresa import EmpresaCreate, EmpresaResponse, EmpresaUpdate
from ..deps import get_current_admin
from ..models.administrador import Administrador

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"],
    dependencies=[Depends(get_current_admin)] # Protege todas as rotas
)

@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED, summary="Cadastra uma nova empresa")
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    """
    Cadastra uma nova empresa cliente na plataforma.
    - **cnpj**: Deve ser único.
    - **email_contato**: Deve ser único.
    """
    db_empresa_cnpj = db.query(Empresa).filter(Empresa.cnpj == empresa.cnpj).first()
    if db_empresa_cnpj:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado.")
        
    db_empresa_email = db.query(Empresa).filter(Empresa.email_contato == empresa.email_contato).first()
    if db_empresa_email:
        raise HTTPException(status_code=400, detail="Email de contato já cadastrado.")

    new_empresa = Empresa(**empresa.dict())
    db.add(new_empresa)
    db.commit()
    db.refresh(new_empresa)
    return new_empresa

@router.get("/", response_model=List[EmpresaResponse], summary="Lista todas as empresas com filtros")
def get_empresas(
    cidade: Optional[str] = Query(None, description="Filtra empresas por cidade"),
    ramo_atuacao: Optional[str] = Query(None, description="Filtra empresas por ramo de atuação"),
    nome: Optional[str] = Query(None, description="Busca textual pelo nome da empresa"),
    db: Session = Depends(get_db)
):
    """
    Lista todas as empresas cadastradas com opções de filtro e busca.
    """
    query = db.query(Empresa)
    if cidade:
        query = query.filter(Empresa.cidade.ilike(f"%{cidade}%"))
    if ramo_atuacao:
        query = query.filter(Empresa.ramo_atuacao.ilike(f"%{ramo_atuacao}%"))
    if nome:
        query = query.filter(Empresa.nome.ilike(f"%{nome}%"))
    
    return query.all()

@router.get("/{empresa_id}", response_model=EmpresaResponse, summary="Detalha uma empresa por ID")
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """
    Exibe os detalhes de uma única empresa através do seu ID.
    """
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return db_empresa

@router.put("/{empresa_id}", response_model=EmpresaResponse, summary="Atualiza os dados de uma empresa")
def update_empresa(empresa_id: int, empresa_update: EmpresaUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de uma empresa, exceto id, cnpj e data de cadastro.
    """
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    update_data = empresa_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_empresa, key, value)
    
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@router.delete("/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Exclui uma empresa")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """
    Remove uma empresa do banco de dados.
    """
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    db.delete(db_empresa)
    db.commit()
    return