from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

from green_bank.api.routers import api_router
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
    return app
