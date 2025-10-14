# Importa a classe 'BaseModel' da biblioteca Pydantic.
# Todos os schemas devem herdar desta classe para obter
# as funcionalidades de validação e serialização de dados.
from pydantic import BaseModel


# --- Schema de Criação de Administrador ---
# Esta classe define a estrutura dos dados que a API espera receber
# ao registar um novo administrador. Funciona como um modelo de validação.
class AdminCreate(BaseModel):
    # O campo 'username' é obrigatório e deve ser do tipo string (texto).
    username: str
    
    # O campo 'password' também é obrigatório e deve ser do tipo string.
    password: str


# --- Schema de Resposta de Administrador ---
# Esta classe define a estrutura dos dados que a API irá enviar de volta
# ao cliente após criar ou obter os dados de um administrador.
# A sua principal função é filtrar os dados, garantindo que informações sensíveis
# (como a senha) nunca sejam expostas.
class AdminResponse(BaseModel):
    # O campo 'id' será incluído na resposta e deve ser um número inteiro.
    id: int
    
    # O campo 'username' também será incluído.
    username: str

    # --- Configuração do Schema ---
    # A classe interna 'Config' permite-nos ajustar o comportamento do Pydantic.
    class Config:
        # 'orm_mode = True' (ou 'from_attributes = True' em versões mais recentes)
        # é uma configuração crucial que permite ao Pydantic criar um schema
        # diretamente a partir de um objeto do SQLAlchemy (como o nosso modelo 'Administrador').
        # Sem isto, teríamos de converter manualmente o objeto da base de dados num dicionário.
        orm_mode = True
