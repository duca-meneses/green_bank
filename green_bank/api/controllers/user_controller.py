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
    '''Create a new user
    ---
    post:
      tags:
        - users
      summary: Create a new user
      description: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateUserSchema
      responses:
        201:
          description: User created
          content:
            application/json:
              schema: UserSchema
        400:
          description: Bad request
          content:
            application/json:
              schema: ErrorSchema
        409:
          description: Conflict
          content:
            application/json:
              schema: ErrorSchema
        422:
          description: Unprocessable Entity
          content:
            application/json:
              schema: ErrorSchema
    '''
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json) # type: ignore
    except ValidationError as error:
        raise GreenBankBasicException(error.messages, HTTPStatus.UNPROCESSABLE_ENTITY)
    user = user_service.create_user(user=data)
    return user, HTTPStatus.CREATED

@app.route('/', methods=['GET'])
def list_users():
    '''List all users
    ---
    get:
      tags:
        - users
      summary: List all users
      description: Retrieve a list of all users
      responses:
        200:
          description: List of users
          content:
            application/json:
              schema: ListUserSchema

    '''
    users = user_service.get_users()
    return {'users': users}, HTTPStatus.OK

@app.route('/<uuid:user_id>', methods=['GET'])
def get_user(user_id):
    '''Get user by id
    ---
    get:
      tags:
        - users
      summary: Get user by ID
      description: Retrieve user details by user ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: string
            format: uuid
          required: true
          description: The ID of the user
      responses:
        200:
          description: User found
          content:
            application/json:
              schema: UserSchema
        404:
          description: User not found
          content:
            application/json:
              schema: ErrorSchema
    '''
    user = user_service.get_user(user_id)
    return user, HTTPStatus.OK

@app.route('/<uuid:user_id>', methods=['PUT'])
def update_user(user_id):
    '''Update user by id
    ---
    put:
      tags:
        - users
      summary: Update user by ID
      description: Update user information using user ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: string
            format: uuid
          required: true
          description: The ID of the user
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateUpdateUserSchema
      responses:
        200:
          description: User updated
          content:
            application/json:
              schema: UpdateUserSchema
        400:
          description: Bad request
          content:
            application/json:
              schema: ErrorSchema
        404:
          description: User not found
          content:
            application/json:
              schema: ErrorSchema
        409:
          description: Conflict
          content:
            application/json:
              schema: ErrorSchema
        422:
          description: Unprocessable Entity
          content:
            application/json:
              schema: ErrorSchema
    '''
    user_schema = CreateUpdateUserSchema()
    data = user_schema.load(request.json) # type: ignore
    user = user_service.update_user(user_id, user=data)
    return user, HTTPStatus.OK

@app.route('/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Delete user by id
    ---
    delete:
      tags:
        - users
      summary: Delete user by ID
      description: Remove a user by their ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: string
            format: uuid
          required: true
          description: The ID of the user
      responses:
        204:
          description: User deleted successfully
        404:
          description: User not found
          content:
            application/json:
              schema: ErrorSchema
    '''
    user_service.delete_user(user_id)
    return {}, HTTPStatus.NO_CONTENT
