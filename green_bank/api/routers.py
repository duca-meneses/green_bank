from flask.blueprints import Blueprint

from green_bank.api.controllers.auth_controller import app as auth_controller
from green_bank.api.controllers.health_check import health_check
from green_bank.api.controllers.user_controller import app as user_controller

api_router = Blueprint('api', __name__)
api_router.register_blueprint(health_check)
api_router.register_blueprint(user_controller)
api_router.register_blueprint(auth_controller)
