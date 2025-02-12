# Green Bank

## Descrição
Green Bank é uma aplicação de exemplo para gerenciamento de usuários e transações financeiras. A aplicação é construída utilizando Flask, SQLAlchemy e Alembic.

## Requisitos
- Python 3.13.0
- Poetry
- Flask
- SqlAlchemy
- Alembic
- Pytest
- Docker

## Instalação

1. Clone o repositório:
    ```sh
    git clone <https://github.com/duca-meneses/green_bank.git>
    cd green_bank
    ```

2. Instale as dependências:
    ```sh
    poetry install
    ```

3. Configure as variáveis de ambiente:
    Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
    ```env
    DATABASE_URL=sqlite:///database.db
    SECRET_KEY=<sua_secret_key>
    JWT_SECRET_KEY=<sua_jwt_secret_key>
    ```

## Uso

1. Execute as migrações do banco de dados:
    ```sh
    alembic upgrade head
    ```

2. Inicie a aplicação:
    ```sh
    poetry run flask run --host=0.0.0.0 --port=5000
    ```

3. Acesse a aplicação em `http://localhost:5000`.

## Estrutura do Projeto

- `green_bank/`: Contém o código fonte da aplicação.
- `migrations/`: Contém os scripts de migração do banco de dados.
- `tests/`: Contém os testes da aplicação.

## Endpoints

### Autenticação
- `POST /api/auth/login`: Realiza o login e retorna um token JWT.
- `PATCH /api/auth/<uuid:user_id>/change-password` Realiza a mudança da senha do usuário

### Usuários
- `POST /api/users/`: Cria um novo usuário.
- `GET /api/users/`: Lista todos os usuários.
- `GET /api/users/<uuid:user_id>`: Obtém um usuário pelo ID.
- `PUT /api/users/<uuid:user_id>`: Atualiza um usuário pelo ID.
- `DELETE /api/users/<uuid:user_id>`: Deleta um usuário pelo ID.

### Health Check
- `GET /`: Verifica a saúde da aplicação.
