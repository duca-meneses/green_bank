from http import HTTPStatus

from flask import request
from flask.blueprints import Blueprint
from marshmallow import ValidationError

from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.schemas.user_schema import (
    CreateUpdateUserSchema,
    CreateUserSchema,
)
from green_bank.application.services.user_service import user_service

app = Blueprint('user', __name__, url_prefix='/api/users')


@app.route('/', methods=['POST'])
def create_user():
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json) # type: ignore
    except ValidationError as error:
        raise GreenBankBasicException(error.messages, HTTPStatus.UNPROCESSABLE_ENTITY)
    user = user_service.create_user(user=data)
    return user, HTTPStatus.CREATED

@app.route('/', methods=['GET'])
def list_users():
    users = user_service.get_users()
    return {'users': users}, HTTPStatus.OK

@app.route('/<uuid:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    return user, HTTPStatus.OK

@app.route('/<uuid:user_id>', methods=['PUT'])
def update_user(user_id):
    user_schema = CreateUpdateUserSchema()
    data = user_schema.load(request.json) # type: ignore
    user = user_service.update_user(user_id, user=data)
    return user, HTTPStatus.OK

@app.route('/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_service.delete_user(user_id)
    return {}, HTTPStatus.NO_CONTENT
