# Arquitetura e Fluxo do Projeto (ckts finance)

Este documento atua como o mapa fiel da base de código do **ckts finance**, evidenciando como os padrões de projeto exigidos foram estritamente aplicados na nossa arquitetura baseada em Python (Flask).

---

## 🏗 Arquitetura Aplicada (MVC + Service Layer + Router + Middleware)

O projeto foge de lógicas monolíticas (como fat controllers) separando responsabilidades nas seguintes pastas reais:

- **`app/routes/` (Router)**: Camada de orquestração de endpoints estruturada em Classes (POO). Associa as URLs HTTP e os Middlewares diretamente aos métodos do Controller. Nenhuma lógica de negócio reside aqui.
- **`app/controllers/` (Controller)**: Camada de controle (C do MVC) que recebe os dados limpos das requisições (via objetos Flask `request`) e despacha para os serviços. Aqui ocorrem as montagens das respostas HTTP (Status Code, JSON).
- **`app/services/` (Service Layer)**: Coração do negócio. Toda a inteligência da aplicação está contida aqui (validações de domínio, cálculos, encriptação JWT/Hash, lógica comercial). Esta camada não acessa o banco de dados via SQL direto; invoca o DAO.
- **`app/models/` (Model / DAO)**: Camada exclusiva para lidar com banco de dados. Contém as Data Access Objects (DAOs). Toda injeção de consulta SQL reside exclusivamente dentro destes arquivos.

### 🧩 Isolamento do Módulo SaaS (Relacionamento N:N)
Para suportar o relacionamento M:N exigido entre Usuários e Planos sem causar acoplamento destrutivo no fluxo já existente de Transações, arquitetamos um módulo paralelo autossuficiente:
- **`PlanoDAO`**, **`PlanoService`** e **`PlanoController`**: Este trio opera isolado, lidando com a tabela `planos` e a tabela associativa `usuario_planos`. Quando um usuário troca de plano, nenhuma lógica financeira de transações é afetada. Essa separação demonstra aderência ao Single Responsibility Principle (SRP) e garante que futuras manutenções na mecânica de pagamento/mensalidade não afetem as despesas diárias dos usuários.

---

## 🧬 Implementação da POO e Interfaces Obrigatórias

Através do módulo `abc` (Abstract Base Classes) do Python nativo (`app/utils/interfaces.py`), estabelecemos um forte contrato de acoplamento (Interface Segregation Principle).

- **`InterfaceDAO`**: Obriga as DAOs filhas a implementarem métodos base para o CRUD (`criar`, `ler`, `atualizar`, `deletar` e `listar`). 
  - *Filhas implementadoras:* `UsuarioDAO`, `TransacaoDAO`, `CategoriaDAO`.

- **`InterfaceController`**: Obriga os controllers a conterem um método genérico `processar_requisicao` de padronização, servindo como classe pai para padronizar todos os receptores do Flask.
  - *Filhas implementadoras:* `UsuarioController`, `TransacaoController`, `CategoriaController`, `LogController`, `AdminController`, `DataController`.

- **`InterfaceService`**: Força a implementação do método `executar_regras_negocio` que assina o contrato da camada de serviço corporativo.
  - *Filhas implementadoras:* `UsuarioService`, `TransacaoService`, `CategoriaService`, `LogService`, `AdminService`, `DataService`.

---

## 🛡 Ciclo de Vida da Requisição e os 4 Middlewares Obrigatórios

O ciclo de vida de uma requisição no backend passa obrigatoriamente por uma "gaiola" de middlewares interceptadores antes mesmo de atingir a porta do Controller. Estes arquivos vivem na pasta `app/middlewares/`.

### 1. `auth_middleware.py` (Autenticação JWT)
- **Onde atua**: Em quase 90% das rotas do sistema.
- **O que faz**: Intercepta a requisição lendo o Header `Authorization`. Verifica a assinatura HMAC do Token JWT. Caso inválido ou expirado, bloqueia o usuário imediatamente com `401 Unauthorized`. Caso válido, popula as variáveis globais de acesso com os dados do assinante para uso nos Controllers.

### 2. `validation_middleware.py` (Validação de Entrada)
- **Onde atua**: Rotas de inserção ou alteração que dependam do Payload (Body `POST`, `PUT`, `PATCH`).
- **O que faz**: Verifica estritamente a integridade e os tipos das chaves do JSON recebido cruzando-as com o dicionário de regras de `schema` passado no decorador. Se tentar enviar uma *string* no lugar de um *inteiro*, o interceptador aborta a rota retornando um `400 Bad Request` detalhado. Evita validações lixo poluidoras nos controllers.

### 3. `log_middleware.py` (Analytics de Tráfego)
- **Onde atua**: Globalmente, em TODAS as requisições atendidas pela API.
- **O que faz**: Mede a latência da requisição, extrai o IP de origem, User-Agent, Status de saída e as rotas acionadas. Empacota estes dados estruturalmente e joga em tempo real para a coleção (`request_logs`) do banco de dados **MongoDB** para alimentar as auditorias estatísticas da área administrativa.

### 4. `error_middleware.py` (Captura Global de Exceções)
- **Onde atua**: Globalmente.
- **O que faz**: Evita a tradicional "Tela de erro 500 do Flask" que expõe a stack trace. Intercepta qualquer exceção bruta não tratada originária do Service/Database, formata a resposta como um JSON amigável e dispara o stack trace silenciosamente para o MongoDB (`error_logs`), para que somente a equipe técnica consiga rastrear anomalias de execução sem vazar vulnerabilidades ao usuário final.
