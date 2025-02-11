from http import HTTPStatus

from flask import request
from flask.blueprints import Blueprint

from green_bank.application.services.user_service import user_service

app = Blueprint('user', __name__, url_prefix='/api/users')


@app.route('/', methods=['POST'])
def create_user():
    data = request.json
    user = user_service.create_user(user=data)
    response = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "user_type": user.user_type,
        "document_number": user.document_number,
        "wallet_balance": user.wallet_balance,
        "created": user.created,
    }
    return response, HTTPStatus.CREATED

@app.route('/', methods=['GET'])
def list_users():
    users = user_service.get_users()
    response = []
    if len(users) == 0:
        return response, HTTPStatus.OK

    for user in users:
        response.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "user_type": user.user_type,
            "document_number": user.document_number,
            "wallet_balance": user.wallet_balance,
            "created": user.created,
        })
    return {'users': response}, HTTPStatus.OK

@app.route('/<uuid:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    response = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "user_type": user.user_type,
        "document_number": user.document_number,
        "wallet_balance": user.wallet_balance,
        "created": user.created,
    }
    return response, HTTPStatus.OK

@app.route('/<uuid:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = user_service.update_user(user_id, user=data)
    response = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created": user.created,
        "updated": user.updated,
    }
    return response, HTTPStatus.OK

@app.route('/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_service.delete_user(user_id)
    return {}, HTTPStatus.NO_CONTENT
