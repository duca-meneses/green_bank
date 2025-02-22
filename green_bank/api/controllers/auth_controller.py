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
    '''Login
    ---
    post:
      tags:
        - auth
      summary: Make Login in application
      description: Make Login in application
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateLoginSchema
      responses:
        200:
          description: Login successful
          content:
            application/json:
              schema: TokenSchema
        400:
          description: Bad request
          content:
            application/json:
              schema: ErrorSchema
        401:
          description: Unauthorized
          content:
            application/json:
              schema: ErrorSchema
        422:
          description: Unprocessable Entity
          content:
            application/json:
              schema: ErrorSchema

    '''

    login_schema = CreateLoginSchema()
    try:
        data = login_schema.load(request.json)
    except ValidationError as error:
        raise GreenBankBasicException(error.messages, HTTPStatus.UNPROCESSABLE_ENTITY)
    access_token = auth_service.login(data['email'], data['password'])

    return access_token, HTTPStatus.OK


@bp.route("/<uuid:user_id>/change-password", methods=["POST"])
def change_password(user_id):
    '''Change password
    ---
    post:
      tags:
        - auth
      summary: Change password
      description: Change password
      parameters:
        - in: path
          name: user_id
          required: true
          description: User ID
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema: PasswordChangeSchema
      responses:
        200:
          description: Password changed successfully
          content:
            application/json:
              schema: MessageSchema
        400:
          description: Bad request
          content:
            application/json:
              schema: ErrorSchema
        404:
          description: Not Found
          content:
            application/json:
              schema: ErrorSchema
        422:
          description: Unprocessable Entity
          content:
            application/json:
              schema: ErrorSchema

    '''

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

    response = auth_service.change_password(user_id, data)

    return response, HTTPStatus.OK
