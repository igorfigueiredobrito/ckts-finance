# Arquitetura e Fluxo de Requisições

Este documento constitui o guia interno oficial que disseca a estrutura sintática, as decisões arquiteturais e o ciclo de vida sistêmico deste software de Controle Financeiro. O seu propósito é ambientar novos engenheiros sobre as diretrizes do código e como as peças se conversam de forma escalar e modular.

---

## Padrão Arquitetural Adotado: MVC Acoplado à Service Layer

Decidimos fugir do clássico — e por vezes frágil — padrão MVC cru. Adoção isolada do MVC frequentemente acaba inchando os `Controllers` com regras de negócios ou permitindo que a `View/Routes` acesse entidades brutas.

Para sanar isso, introduzimos a **Service Layer (Camada de Serviços)**. O fluxo tornou-se mais inteligente:
1. O **Controller** é burro: Sabe apenas converter HTTP para Python e Python para JSON. 
2. O **Service** é o cérebro: Processa as regras de negócio intrínsecas ao projeto (ex: calcular totais, vetar valores negativos, autorizar acessos).
3. O **DAO (Data Access Object)** é o braço forte: Só ele tem autorização formal para tocar as conexões SQL.

---

## O Ciclo de Vida de uma Requisição

Qual é o caminho dos dados quando o cliente final clica no botão azul de "Salvar Transação" até ele ser persistido no disco de servidor?

1. **Frontend (Vue.js)**
   O usuário preenche os campos num *Glass Modal*. O Javascript intercepta os dados via função assíncrona, verifica superficialmente os preenchimentos e monta o Payload JSON, anexando o *Token JWT* armazenado em `localStorage` nos cabeçalhos da requisição através do Axios.
   
2. **Rota / Roteador Flask (`app/routes/`)**
   A requisição aterrissa em um sub-roteador específico. Nele, decoradores interceptam o pacote de dados primeiro.
   
3. **Pátio dos Middlewares**
   - *Auth Middleware:* Bloqueia ou extrai o JWT, destrinchando o ID e colando no escopo global (`g.usuario_id`).
   - *Log Middleware:* Monitora de forma passiva o Timestamp e URL para auditoria de tráfego.
   - *Error Middleware:* Se algo não previsto acontecer do passo 4 em diante, ele amortece e emite JSON polidos sem vazar stack trace ao cliente, salvando o log bruto no MongoDB.
   
4. **O Controller (`app/controllers/`)**
   A função `TransacaoController.criar()` arranca as entranhas JSON e aciona o Service.
   
5. **O Service (`app/services/`)**
   O Service checa as lógicas cruciais. A transação enviada tentou passar R$ -10.00? O service levanta um erro de infraestrutura limpo. Passou nos testes? Ele empurra os dados ao DAO.
   
6. **O DAO + Bancos de Dados (`app/models/` + `app/utils/`)**
   O `TransacaoDAO` recebe o contrato já sanitizado. Ele invoca a string SQL paramétrica via DB Helper (evitando Injections). **Persistência ocorrida no MySQL.** 
   Logo na linha de baixo, o Service notifica o `mongo_db.py`, armazenando um artefato de histórico de alteração do sistema no Banco Não-Relacional.
   
7. **Caminho de Volta (Return JSON)**
   O Controller empacota tudo na função `jsonify()`. O Axios do Vue.js capta a promessa revolvida (`status 200/201`), exibe o alerta silencioso verde ao usuário e re-renderiza o DOM via reatividade de variáveis do Vue.

---

## Dicionário de Camadas e Classes

Um guia rápido da nomenclatura de pastas na nossa aplicação Python:

### `/utils/interfaces.py`
Nossa bússola mor. O Python não possui interfaces nativas explícitas, por isso estendemos o módulo `abc.ABC`. Aqui, o `InterfaceDAO`, `InterfaceService` e `InterfaceController` sentenciam os verbos que qualquer entidade posterior OBRIGATORIAMENTE terá de implementar (criar, ler, listar, etc). É a "garantia de contrato".

### `/middlewares/`
Nossos porteiros sistêmicos.
- `auth_middleware.py`: Garante as chaves da casa. Decodifica o payload do Token.
- `log_middleware.py`: Metrifica quanto tempo o request levou a responder para relatórios analíticos de performance.
- `error_middleware.py`: Capa de super-herói que engole as chamas do sistema. Exceções nativas entram por aqui e viram avisos carinhosos ao Front-End.

### `/routes/`
Agrupamentos (ou Blueprints) focados. Separam fisicamente o domínio `/api/usuarios` de `/api/transacoes`, tornando a injeção na aplicação matriz em `app/__init__.py` extremamente limpa.

### `/controllers/`
Especialistas em Protocolo. Eles não validam que 1+1=2. Eles apenas checam se o "Verbo HTTP" era de fato um POST, e se o corpo da requisição é interpretável. O resto, eles delegam.

### `/services/`
A regra corporativa. Arquivos massos que contêm, por exemplo: lógica da geração de XML, verificação minuciosa se um arquivo provindo de upload é genuinamente JSON, hashing de senhas.

### `/models/`
O acesso cru, frio e direto aos bits no Banco. O DAO (`Data Access Object`) foca em conexões Singleton velozes em pool com queries exatas de CRUD.

---

## Estratégia Híbrida: O Porquê de MySQL + MongoDB

Adotar bancos de natureza discrepante não foi acaso: foi estratégico.

**MySQL (Banco Relacional)**
Utilizado para Entidades Fixas. Precisávamos amarrar usuários a dezenas de transações e transações a dezenas de tags. Integridade referencial é fundamental. Restrições como `ON DELETE CASCADE` ou `ON DELETE RESTRICT` só funcionam de fato num banco de escopo relacional rígido.

**MongoDB (NoSQL Document-Oriented)**
Utilizado para os Bastidores. Auditoria e Logs geram *gigabytes* de detritos não estruturados, empilhando relatórios dinâmicos de erros. Colocar esse tráfego pesado nas costas de tabelas transacionais no MySQL causa lentidão em Join Tables e estouro do DBSpace. Documentos flexíveis em coleções Mongo tornaram o acompanhamento de incidentes imensuravelmente mais ágil.
