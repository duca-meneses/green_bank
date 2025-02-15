from flask.blueprints import Blueprint

from .controllers.auth_controller import bp as auth_controller
from .controllers.health_check import health_check
from .controllers.transaction_controller import transaction
from .controllers.user_controller import app as user_controller

api_router = Blueprint('api', __name__)
api_router.register_blueprint(health_check)
api_router.register_blueprint(user_controller)
api_router.register_blueprint(auth_controller)
api_router.register_blueprint(transaction)
