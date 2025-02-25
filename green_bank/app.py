from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint

from green_bank.api.routers import api_router, spec
from green_bank.api.spec import register_routes_with_spec
from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.errors.handler.error_handling import error_handling
from green_bank.infra.security import bcrypt
from green_bank.infra.settings import Settings

jwt = JWTManager()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    app.secret_key = Settings().SECRET_KEY
    app.config['JWT_SECRET_KEY'] = Settings().JWT_SECRET_KEY
    app.register_error_handler(GreenBankBasicException, error_handling)
    app.register_blueprint(api_router)


    register_routes_with_spec(app)

    @app.route('/api/docs/')
    def swagger():

        return spec.to_dict()


    SWAGGER_URL = Settings().SWAGGER_UI_URL
    API_DOCS_URL = Settings().API_DOC_URL

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_DOCS_URL,
        config={'app_name': Settings().API_TITLE}
    )

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


    return app
