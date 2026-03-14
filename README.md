# backend-cadastro-servicos

API REST desenvolvida com FastAPI para gerenciamento de serviços/tarefas com autenticação baseada em JWT.

O projeto permite que usuários se cadastrem, façam login e gerenciem seus próprios serviços, incluindo criação, atualização e filtros por cliente ou data.

Este projeto foi desenvolvido com foco em aprendizado de backend com Python, aplicando conceitos de autenticação, organização de código e integração com banco de dados.

🚀 Tecnologias utilizadas

- Python

- FastAPI

- SQLAlchemy

- SQLite

- JWT (python-jose)

- pwdlib (hash de senha)

- Pydantic

- dotenv

📂 Estrutura do projeto
FUTURO-Tasks
│
├── main.py
├── database.py
├── dependencies.py
│
├── models.py
├── schemas.py
│
├── security.py
│
├── auth_routers.py
└── task_routers.py
🔐 Autenticação

A API utiliza autenticação baseada em JWT (JSON Web Token).

Fluxo:

Usuário realiza login

API retorna:

access_token

refresh_token

O access_token é utilizado para acessar rotas protegidas.

Quando expira, o refresh_token pode gerar um novo token de acesso.

👤 Funcionalidades de Usuário

- Cadastro de usuário
- Login com autenticação JWT
- Atualização parcial de perfil (PATCH)
- Validação de CPF e telefone

📋 Funcionalidades de Serviços

Usuários autenticados podem:

- Criar serviços
- Atualizar serviços
- Listar seus próprios serviços
- Filtrar serviços por:
- nome do cliente
- data do serviço
- prazo

Cada serviço pertence apenas ao usuário que o criou.

🔎 Exemplo de rotas
- Cadastro de usuário
- POST /users/cadastro
- Login
- POST /users/login

Retorna:

- access_token
- refresh_token
- Criar serviço
- POST /servico/cadastrar_servico
- Atualizar serviço
- PATCH /servico/atualizar_servico/{id}
- Listar serviços
- GET /servico/meus_servicos

Filtros disponíveis:

?nome_cliente=joao
?data_servico=2026-03-10
?prazo=2026-03-20


⚙️ Como rodar o projeto
1️⃣ Clonar o repositório
git clone https://github.com/seuusuario/futuro-tasks.git
2️⃣ Instalar dependências
pip install -r requirements.txt
3️⃣ Criar arquivo .env (Baseie-se no .env.example.)

4️⃣ Rodar o servidor
uvicorn main:app --reload
5️⃣ Acessar documentação automática
http://127.0.0.1:8000/docs
