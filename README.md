# 🌵 Caktus finance (SaaS de Controle Financeiro)

**Autores:** Igor Brito e João Brandão

Bem-vindo ao repositório do **ckts finance**, um SaaS (Software as a Service) completo de gestão e controle financeiro pessoal. Este projeto foi concebido para entregar uma experiência premium ao usuário através de uma arquitetura altamente escalável, aplicando rigorosamente conceitos de Arquitetura de Software e Programação Orientada a Objetos.

---

## 🌟 Funcionalidades Principais

- **Dashboard Financeiro Dinâmico:** Gráficos interativos (Chart.js) detalhando receitas e despesas.
- **Módulo Financeiro Pessoal:** Controle transacional, gerenciamento de categorias e exportação de PDF.
- **Gestão de Planos SaaS (Admin) e Assinaturas (Usuário):** Sistema N:N de upgrade/downgrade de planos (Básico, Pro, Premium).
- **Importação e Exportação (JSON/XML):** Capacidade de backup dos dados em lote e extração de logs do MongoDB.

---

## 🛠 Stack Tecnológico

A aplicação adota uma divisão clara entre frontend e backend, garantindo responsividade, segurança e organização.

- **Frontend:** Vue.js 3 (Composition API, Vite, Router)
- **Backend:** Python 3 (Flask Framework)
- **Banco de Dados Relacional:** MySQL (arquitetura estruturada rigorosamente em 5 tabelas operacionais, incluindo o relacionamento funcional **N:N** que conecta usuários ao ecossistema SaaS).
- **Banco de Dados NoSQL:** MongoDB (para armazenamento de dados não estruturados de Logs e Auditoria de alta performance)

---

## 🎯 Cumprimento de Requisitos Arquiteturais

A tabela abaixo evidencia o cumprimento rigoroso dos requisitos do projeto universitário através da arquitetura aplicada:

| Requisito do Projeto | Nível de Aplicação | Arquivo/Pasta Referência | Status |
| :--- | :--- | :--- | :---: |
| **Arquitetura (MVC + Service Layer + Router + Middleware)** | Separação estrita de camadas. Regras de negócio restritas aos Services. Endpoints gerenciados por Routers dedicados. Consultas no Banco confinadas aos DAOs. | `backend/app/` (separação em models, controllers, services, middlewares e routes) | ✅ |
| **Interfaces Obrigatórias (POO)** | Módulo nativo `abc` do Python. Implementação das classes abstratas `InterfaceDAO`, `InterfaceController` e `InterfaceService`. | `backend/app/utils/interfaces.py` | ✅ |
| **Router Estruturado (POO)** | As rotas aboliram o anti-pattern de funções soltas e estão registradas dinamicamente dentro de classes dedicadas (`UsuarioRouter`, `AdminRouter`, etc). | `backend/app/routes/` | ✅ |
| **Middlewares (Interceptadores)** | Uso obrigatório de 4 middlewares operacionais integrados: Auth (JWT), Log (Mongo), Error (Global JSON), Validation (Payload Schema Validator). | `backend/app/middlewares/` | ✅ |

---

## 🚀 Como Executar o Projeto Localmente (macOS)

Abra o seu terminal no macOS e execute os passos a seguir:

### 1. Iniciar o Banco de Dados
Certifique-se de que os serviços do **MySQL** (na porta 3306) e do **MongoDB** (na porta 27017) estão ativos no seu ambiente local. 
Rode o script `database.sql` contido na raiz do projeto para subir as tabelas estruturais.

### 2. Rodar o Backend (API Flask)

```bash
# 1. Entre na pasta do backend
cd ckts-finance/backend

# 2. Ative o ambiente virtual (venv)
source venv/bin/activate

# 3. Instale as dependências (caso seja a primeira execução)
pip install -r requirements.txt

# 4. Inicie o Servidor da API na porta 5001
python run.py
```

### 3. Rodar o Frontend (Vue.js)
Abra uma **nova aba de terminal** mantendo o servidor backend rodando na anterior.

```bash
# 1. Entre na pasta do frontend
cd ckts-finance/frontend

# 2. Instale os pacotes Node (caso seja a primeira execução)
npm install

# 3. Inicie o Servidor de Desenvolvimento
npm run dev
```

Após executar, acesse no seu navegador o endereço fornecido no terminal (geralmente `http://localhost:5173`) e teste a plataforma.
