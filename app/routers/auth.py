from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models.administrador import Administrador
from ..schemas.administrador import AdminCreate, AdminResponse
from ..schemas.token import Token
from ..services import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

@router.post("/register", response_model=AdminResponse, status_code=status.HTTP_201_CREATED, summary="Registra um novo administrador")
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(Administrador).filter(Administrador.username == admin.username).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Username já registrado.")
    
    hashed_password = auth_service.get_password_hash(admin.password)
    new_admin = Administrador(username=admin.username, hashed_password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

@router.post("/login", response_model=Token, summary="Realiza o login e retorna um token JWT")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(Administrador).filter(Administrador.username == form_data.username).first()
    if not admin or not auth_service.verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(
        data={"sub": admin.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}