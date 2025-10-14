# Importa a classe 'BaseModel' da biblioteca Pydantic.
from pydantic import BaseModel


# --- Schema do Token de Acesso ---
# Esta classe define a estrutura exata do objeto JSON que a sua API irá devolver
# ao cliente após um login bem-sucedido.
class Token(BaseModel):
    # O 'access_token' é o token JWT (JSON Web Token) em si. É uma longa string
    # que o cliente deverá guardar e enviar em pedidos futuros para se autenticar.
    access_token: str
    
    # O 'token_type' informa ao cliente como o token deve ser usado.
    # O padrão para JWT é "bearer", o que significa que "quem tiver este token
    # (o portador/bearer) está autorizado".
    token_type: str


# --- Schema dos Dados Dentro do Token ---
# Esta classe representa a estrutura dos dados que estão guardados *dentro* do payload do JWT.
# Ela não é devolvida ao cliente, mas sim usada internamente pela sua API
# para validar o token e extrair as informações dele (como o nome do utilizador).
class TokenData(BaseModel):
    # O campo 'username' corresponde ao "subject" (sub) que definimos ao criar o token.
    # 'str | None = None' é uma forma moderna de dizer que este campo pode ser uma string
    # ou pode ser Nulo (None), com o valor padrão sendo None. Isto ajuda a tratar
    # casos em que o token possa estar malformado ou não conter o username.
    username: str | None = None