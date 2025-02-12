from http import HTTPStatus

from flask import Blueprint, request
from marshmallow import ValidationError

from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.schemas.auth_schema import (
    CreateLoginSchema,
    PasswordChangeSchema,
)
from green_bank.application.services.auth_service import auth_service

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route("/login", methods=["POST"])
def login():
    login_schema = CreateLoginSchema()
    try:
        data = login_schema.load(request.json)
    except ValidationError as error:
        raise GreenBankBasicException(error.messages, HTTPStatus.UNPROCESSABLE_ENTITY)
    access_token = auth_service.login(data['email'], data['password'])

    return access_token, HTTPStatus.OK


@bp.route("/<uuid:user_id>/change-password", methods=["Patch"])
def change_password(user_id):
    password_schema = PasswordChangeSchema()
    try:
        data = password_schema.load(request.json)

        if data['new_password'] != data['new_password_confirm']:
            raise GreenBankBasicException(
                "Passwords do not match",
                HTTPStatus.UNPROCESSABLE_ENTITY
            )
    except ValidationError as error:
        raise GreenBankBasicException(error.messages, HTTPStatus.UNPROCESSABLE_ENTITY)

    auth_service.change_password(user_id, data)

    return {'message': 'Password changed successfully'}, HTTPStatus.OK
