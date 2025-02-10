from flask import Flask

from green_bank.api import routers


app = Flask(__name__)


app.register_blueprint(routers.api_router)