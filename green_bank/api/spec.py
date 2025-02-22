from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask

tags = [
    {'name': 'auth', 'description': 'Operations related to authentication'},
    {'name': 'health check', 'description': 'Operations related to health check'},
    {'name': 'users', 'description': 'Operations related to users'},
    {'name': 'transactions', 'description': 'Operations related to transactions'},
]
spec = APISpec(
    title='Green Bank API',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    tags = tags,
)

api_key_scheme = {'type': 'apiKey', 'in': 'header', 'name': 'X-API-Key'}

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
