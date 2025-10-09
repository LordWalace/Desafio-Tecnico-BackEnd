# API e Portal de Gestão de Clientes - Ecomp Jr.

<div align="center">
  <img src="https://imgur.com/8DjSWjX.png" alt="Logo EcompJr" width="200px">
</div>

Este projeto é uma solução **full-stack** desenvolvida como parte do **Desafio Técnico - Processo Seletivo 2025.2 da Ecomp Jr.**  
Ele consiste numa **API RESTful** para gestão de empresas clientes e numa **interface de front-end** para interagir com a API.

---

## 🚀 Tecnologias Utilizadas

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

## 📋 Pré-requisitos

Antes de começar, certifique-se de que tem os seguintes programas instalados na sua máquina:

- **Python** (versão 3.11 ou superior)  
- **Node.js** (versão LTS recomendada)  
- **PostgreSQL** (servidor de base de dados)  

---

## ⚙️ Como Executar o Projeto

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

## 4. Observações
- Crie o ambiente virtual na raiz do projeto e utilize-o para instalar as dependências do backend.
- O backend deve estar rodando para o frontend se comunicar normalmente com a API.
- Senhas para autenticação devem ter até 72 caracteres.
- O frontend não possui variáveis de ambiente — basta instalar as dependências e rodar.

-O frontend estará disponível em:  
http://localhost:5173

-A API estará disponível em:
http://localhost:8000. Você pode acessar a documentação da API em http://localhost:8000/docs.