from flask import Flask
from flask_jwt_extended import JWTManager

from green_bank.api import routers
from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.errors.handler.error_handling import error_handling
from green_bank.infra.settings import Settings

app = Flask(__name__)
jwt = JWTManager(app)

app.secret_key = Settings().SECRET_KEY
app.config['JWT_SECRET_KEY'] = Settings().JWT_SECRET_KEY
app.register_error_handler(GreenBankBasicException, error_handling)
app.register_blueprint(routers.api_router)
