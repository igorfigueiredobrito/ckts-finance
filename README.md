# Sistema de Controle Financeiro Pessoal

Um robusto sistema web *Full Stack* voltado para o controle detalhado das finanças pessoais. Desenvolvido com uma arquitetura moderna e rigorosa (MVC + Service Layer com abstração via Interfaces), o projeto visa oferecer segurança, alto desempenho e auditoria granular. 

Este projeto atende e excede requisitos acadêmicos estritos, integrando perfeitamente bancos relacionais e não-relacionais sob um *Premium UI/UX Design* rico em Glassmorphism.

---

## 👨‍💻 Autores

**Igor Figueiredo Brito**  
**Joao Vitor Brandao**
Estudantes de Engenharia da Computação.

---

## 🛠️ Tecnologias Utilizadas

A arquitetura foi meticulosamente dividida nas seguintes vertentes tecnológicas:

| Camada / Função | Tecnologias Principais | Descrição e Propósito |
| :--- | :--- | :--- |
| **Backend** | Python 3, Flask | Núcleo do sistema, focado em alta coesão e baixo acoplamento via OOP. |
| **Frontend** | Vue.js 3 (Composition API), Vite | Criação de SPA (*Single Page Application*) reativa. |
| **Estilização** | CSS3 (Vanilla), Lucide Icons | Design System *Premium Dark Mode* e Animações fluidas. |
| **Banco Relacional** | MySQL | Entidades, transações, usuários e lógica relacional de negócio. |
| **Banco Analítico** | MongoDB | Armazenamento de alta performance para auditoria e *Logs* globais. |
| **Segurança e JWT**| PyJWT, bcrypt, Cryptography | Hash seguro de senhas e autenticação Stateless. |
| **Extras Frontend** | Chart.js, vue-chartjs | Componentização de gráficos dinâmicos no Dashboard. |
| **Extras Frontend** | jsPDF, jspdf-autotable | Renderização de Relatórios em PDF nativamente no Browser. |

---

## ✅ Checklist de Requisitos

O sistema cumpre com maestria os seguintes pontos:

- [x] **Arquitetura Orientada a Objetos**: Camadas MVC rigorosamente baseadas em Classes Abstratas (`abc`).
- [x] **Middlewares Completos**: Autenticação, Interceptação Global de Erros, Validação de Payloads e Registro de Performance.
- [x] **Banco MySQL Integrado**: Script inicial `database.sql` contemplando 5 tabelas com relacionamento (1:N, N:N) e Constraints Restritivas.
- [x] **MongoDB Integrado**: Utilizado estritamente para Logs Analíticos (CRUD) e Registro de Exceções Críticas.
- [x] **CRUD Completo**: Adicionar, Ler, Atualizar, Filtrar e Deletar Transações de forma assíncrona.
- [x] **Upload de Arquivos**: Persistência física de avatares / fotos de perfil.
- [x] **Importação Dinâmica**: Suporte a envio de `.json` em lote com tratamento pacífico de erros.
- [x] **Exportação Dinâmica**: Download nativo das entidades via `.json` e auditoria em `.xml`.
- [x] **Dashboard Estatístico**: Integração transparente do *Chart.js* via requisições API.
- [x] **Relatórios PDF**: Exportação sob demanda e com injeção de parâmetros de filtro aplicados pelo usuário.

---

## 🚀 Como Executar o Projeto (macOS / Linux Terminal)

O passo a passo foi modelado para terminais Unix/macOS.

### 1. Preparando o Banco de Dados
1. Certifique-se de ter o MySQL e o MongoDB rodando localmente (seja via *brew services*, Docker ou de forma nativa).
2. Conecte-se ao seu MySQL via terminal:
   ```bash
   mysql -u root -p
   ```
3. Copie o conteúdo do script SQL da nossa raiz e cole no terminal para que as 5 tabelas base sejam erguidas perfeitamente.

### 2. Levantando o Backend (Flask)
Abra um terminal e acesse a raiz do projeto:

```bash
# 1. Acesse a pasta exclusiva do ecossistema Python
cd backend

# 2. Crie o Ambiente Virtual (Virtual Environment)
python3 -m venv venv

# 3. Ative o Ambiente Virtual
source venv/bin/activate

# 4. Instale as dependências rigorosas do projeto
pip install -r requirements.txt

# 5. Ajuste suas credenciais no arquivo .env (se necessário)

# 6. Inicie o Servidor Backend (rodará na porta 5000)
python run.py
```

### 3. Levantando o Frontend (Vue.js)
Mantenha o terminal do Backend rodando e abra uma nova aba (ou janela) no terminal:

```bash
# 1. Acesse o subdiretório do frontend
cd frontend

# 2. Instale todas as dependências JavaScript do Node
npm install

# 3. Inicie o servidor de desenvolvimento (Vite)
npm run dev
```

Pronto! Acesse o link que o Vite retornará (geralmente `http://localhost:5173`) e desfrute do sistema financeiro.
