from http import HTTPStatus
from flask import Blueprint, request

from green_bank.application.services.auth_service import auth_service

app = Blueprint('auth', __name__, url_prefix='/api/auth')

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("email", None)
    password = request.json.get("password", None)

    access_token = auth_service.login(username, password)   

    
    return {'access_token': access_token}, HTTPStatus.OK