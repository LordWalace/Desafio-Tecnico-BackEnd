# API e Portal de Gestão de Clientes - Ecomp Jr.

<div align="center">
  <img src="https://imgur.com/8DjSWjX.png" alt="Logo EcompJr" width="200px">
</div>

Este projeto é uma solução **Full-Stack** desenvolvida como parte do **Desafio Técnico - Processo Seletivo 2025.2 da Ecomp Jr.**, para a trilha **Back-End**.  
A aplicação foi criada com foco em **boas práticas de desenvolvimento**, **arquitetura escalável** e **integração eficiente entre backend e frontend**.

---

## Visão Geral

A aplicação consiste em dois módulos principais:

- ** Backend (API):** Sistema de gestão de empresas clientes com operações **CRUD completas**, autenticação via **JWT** e persistência de dados em **PostgreSQL**.  
- ** Frontend (Interface Web):** Painel interativo desenvolvido com **React.js**, **Vite** e **Tailwind CSS**, permitindo a visualização, filtragem e gerenciamento de dados de forma prática e intuitiva.

---

## Funcionalidades

### Back-end (API)
- Sistema de autenticação de administradores com **tokens JWT**.  
- Operações **CRUD** (Criar, Ler, Atualizar, Excluir) completas para a gestão de **empresas clientes**.  
- Sistema de consulta avançada com filtros por **cidade**, **ramo de atuação** e **busca por nome**.  
- Validação de dados e tratamento de erros com **respostas HTTP apropriadas**.  
- Configuração de segurança usando **variáveis de ambiente** para proteger dados sensíveis.

### Front-end (Interface)
- Interface reativa para **login e logout** de administradores.  
- Painel de controle para **visualizar, filtrar e pesquisar** empresas.  
- **Formulários em modal** para adicionar e editar empresas de forma intuitiva.  
- **Confirmação de exclusão** para evitar a perda acidental de dados.

---

## Tecnologias Utilizadas

Este projeto é um **monorepo** dividido em duas partes principais: **backend** e **frontend**.

### Backend (API)
- **Python 3.11+**
- **FastAPI**: Framework web para a construção da API.
- **PostgreSQL**: Base de dados relacional para o armazenamento dos dados.
- **SQLAlchemy**: ORM para a comunicação com a base de dados.
- **JWT (JSON Web Tokens)**: Para autenticação e proteção das rotas.
- **Uvicorn**: Servidor ASGI para executar a aplicação FastAPI.

### Frontend (Portal)
- **React**: Biblioteca para a construção da interface de utilizador.
- **Vite**: Ferramenta de build e servidor de desenvolvimento de alta performance.
- **Tailwind CSS**: Framework de CSS para uma estilização rápida e moderna.
- **npm**: Gestor de pacotes do Node.js.

---

## Pré-requisitos

Antes de começar, certifique-se de que tem os seguintes programas instalados na sua máquina:

- **Python** (versão 3.11 ou superior)  
- **Node.js** (versão LTS recomendada)  
- **PostgreSQL** (servidor de base de dados)  

---

## Como Executar o Projeto

## 1. Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
```

## 2. Backend

### 2.1. Criar e ativar ambiente virtual
```bash
python -m venv venv
```

### No Windows:
```bash
venv\Scripts\activate
```

### No macOS/Linux:
```bash
source venv/bin/activate
```

### 2.2. Instalar dependências
```bash
cd backend
pip install -r requirements.txt
```

### 2.3. Configurar variáveis de ambiente
Crie o arquivo `.env` dentro da pasta `backend` com o seguinte conteúdo:

```env
SECRET_KEY = sua chave secreta
DATABASE_URL = postgresql://usuario:senha@localhost:5432/nome_do_banco
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = HS256
```

### 2.4. Rodar o servidor FastAPI
```bash
uvicorn app.main:app --reload
```

Ajuste `app.main:app` conforme o caminho do arquivo e do objeto FastAPI do seu projeto.

## 3. Frontend

### 3.1. Instalar dependências
```bash
cd ../frontend
npm install
```

### 3.2. Rodar o projeto
```bash
npm run dev
```

## 4. EndPoints

### 4.1 Autenticação
- POST /auth/register: Regista um novo administrador.

  - Corpo: 
  ```json 
    { "username": "seu_user", 
      "password": "sua_senha" }
  ```

- POST /auth/login: Autentica um administrador e retorna um token JWT.

  - Corpo: ```username = seu_user & password = sua_senha (formato x-www-form-urlencoded)```

### 4.2 Empresas (Requer Token de Autenticação)
- GET /empresas/: Lista todas as empresas.

  - Query Params (opcionais): ```? nome = Tech & cidade = Feira & ramo_atuacao = Software```

- POST /empresas/: Cria uma nova empresa.

  - Corpo: 
  ```json 
  { "nome": "Nova Empresa",
    "cnpj": "12345678000195",
    "cidade": "Cidade",
    "ramo_atuacao": "Tecnologia",
    "telefone": "75999999999",
    "email_contato": "contato@novaempresa.com" }
  ```

- GET /empresas/{empresa_id}: Obtém os detalhes de uma empresa específica.

  - Parâmetro de Caminho: {empresa_id} (inteiro) - O ID da empresa a ser procurada.

  - Resposta de Sucesso (200 OK): Um objeto JSON com os dados da empresa.

  - Resposta de Erro (404 Not Found): Se a empresa com o ID fornecido não for encontrada.

- PUT /empresas/{empresa_id}: Atualiza os dados de uma empresa.

  - Corpo: 
  ```json
  { "nome": "Nome Atualizado",
    "cidade": "Nova Cidade",
    ... }
  ```

- DELETE /empresas/{empresa_id}: Exclui uma empresa.

  - Parâmetro de Caminho: {empresa_id} (inteiro) - O ID da empresa a ser excluída.

  - Resposta de Sucesso (204 No Content): A resposta não tem conteúdo, a indicar que a exclusão foi bem-sucedida.

# 5. Observações / Avisos

### Ambiente virtual
- Crie o ambiente virtual **na raiz do projeto**.  
- Utilize-o **apenas** para instalar as dependências do **backend**.

### Execução do backend
- O backend precisa estar em execução para que o frontend consiga se comunicar corretamente com a API.

### Senhas de autenticação
- As senhas devem conter **até 72 caracteres**.

### Backend
- Após iniciar, o backend estará disponível em:  
  [http://localhost:8000](http://localhost:8000)  
- A documentação interativa da API (Swagger UI) pode ser acessada em:  
  [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend
- O frontend **não possui variáveis de ambiente** — basta instalar as dependências e rodar o projeto.  
- Após iniciar, o frontend estará disponível em:  
  [http://localhost:5173](http://localhost:5173)