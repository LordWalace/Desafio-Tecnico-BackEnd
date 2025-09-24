# API e Portal de Gestão de Clientes - Ecomp Jr.

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

### 1. Clonar o Repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
---

### 2. Configurar o Backend
Primeiro, vamos configurar e iniciar o servidor da API.

```bash
# 1. Navegue para a pasta do backend
cd backend

# 2. Crie e ative um ambiente virtual
python -m venv venv
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# 3. Instale as dependências do Python
pip install -r requirements.txt
