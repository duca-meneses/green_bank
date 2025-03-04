from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask

from green_bank.infra.settings import Settings

tags = [
    {'name': 'auth', 'description': 'Operations related to authentication'},
    {'name': 'health check', 'description': 'Operations related to health check'},
    {'name': 'users', 'description': 'Operations related to users'},
    {'name': 'transactions', 'description': 'Operations related to transactions'},
]
spec = APISpec(
    title=Settings().API_TITLE,
    version='1.0.0',
    openapi_version='3.0.2',
    info={
        "x-summary": "Green Bank API - Sistema de Pagamentos Simplificado",
        "description": """
### Green Bank API
O **Green Bank API** é um sistema de pagamentos simplificado que permite a realização de transferências entre usuários.

#### 🔑 **Autenticação**
- A autenticação é feita via **JWT Bearer Token**.

#### 🔄 **Principais Operações**
- 🆕 Criar usuários
- 💸 Realizar transferências
- 📜 Listar usuários e transações

#### 🛠 **Tecnologias Utilizadas**
- Flask 🚀
- Flask-JWT-Extended 🔐
- SQLAlchemy 🛢
- Marshmallow 📝

🔗 **Mais informações**:  
[📂 GitHub - Green Bank](https://github.com/duca-meneses/green_bank)
        """,
        "termsOfService": "https://github.com/duca-meneses/green_bank/blob/main/README.md",
        "contact": {
            "name": "Carlos Eduardo Meneses",
            "email": "ducameneses16@gmail.com",
            "url": "https://github.com/duca-meneses",
        },
        "license": {
            "name": "MIT License",
            "url": "https://github.com/duca-meneses/green_bank",
        },
    },

    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    tags=tags
)

api_key_scheme = {
    'type': 'http',
    'in': 'header',
    'scheme': 'bearer',
    'bearerFormat': 'JWT',
    'description': 'Enter your JWT token in the format.'
        'Example: `value: <your-token>`'}

def register_routes_with_spec(app: Flask):
    '''Registra todas as rotas do Flask no `spec`'''
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':  # Ignorar arquivos estáticos
                continue

            view_func = app.view_functions[rule.endpoint]

            if view_func:
                try:
                    spec.path(view=view_func)
                except Exception as e:
                    print(f"Erro ao registrar {rule.endpoint}: {e}")
