from http import HTTPStatus
from uuid import UUID

from flask import request
from flask.blueprints import Blueprint
from marshmallow import ValidationError

from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.schemas.transaction_schema import CreateTransactionSchema
from green_bank.application.services.transaction_service import transaction_service

transaction = Blueprint('transaction', __name__, url_prefix='/api/transactions')


@transaction.route('/transfer', methods=['POST'])
def create_transfer():
    '''Create a new transaction
    ---
    post:
      security:
        - APIKeyAuth: []
      tags:
        - transactions
      summary: Create a new transaction
      description: Create a new transaction
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateTransactionSchema
      responses:
        201:
          description: Transaction created
          content:
            application/json:
              schema: TransactionSchema
        400:
          description: Bad request
          content:
            application/json:
              schema: ErrorSchema
        401:
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Missing Authorization Header
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

    transaction_schema = CreateTransactionSchema()
    try:
        transaction = transaction_schema.load(request.json)
    except ValidationError as error:
        raise GreenBankBasicException(error.messages, HTTPStatus.UNPROCESSABLE_ENTITY)
    transaction_response = transaction_service.create_transaction(transaction)
    return transaction_response, HTTPStatus.CREATED

@transaction.route('/', methods=['GET'])
def list_transactions():
    '''List transactions
    ---
    get:
      security:
        - APIKeyAuth: []
      tags:
        - transactions
      summary: List transactions
      description: Retrieve a list of transactions,
        optionally filtering by payer or payee name.
      parameters:
        - name: payer_name
          in: query
          description: Filter transactions by payer name
          required: false
          schema:
            type: string
        - name: payee_name
          in: query
          description: Filter transactions by payee name
          required: false
          schema:
            type: string
      responses:
        200:
          description: Transactions retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  transactions:
                    type: array
                    items:
                      $ref: "#/components/schemas/TransactionSchema"
        401:
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Missing Authorization Header
    '''
    payer_name = request.args.get('payer_name', '')
    payee_name = request.args.get('payee_name', '')

    if not isinstance(payer_name, str):
        payer_name = ''
    if not isinstance(payee_name, str):
        payee_name = ''

    transactions = transaction_service.list_transactions(payer_name, payee_name)
    return {'transactions': transactions}, HTTPStatus.OK

@transaction.route('/<uuid:transaction_id>', methods=['GET'])
def get_transaction(transaction_id: UUID):
    '''Get a transaction by id
    ---
    get:
      security:
        - APIKeyAuth: []
      tags:
        - transactions
      summary: Get a transaction by id
      description: Get a transaction by id
      parameters:
        - name: transaction_id
          in: path
          schema:
            type: string
            format: uuid
          required: true
          description: Transaction id
      responses:
        200:
          description: Transaction
          content:
            application/json:
              schema: TransactionSchema
        401:
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Missing Authorization Header
        404:
          description: Transaction not found
          content:
            application/json:
              schema: ErrorSchema
    '''
    transaction = transaction_service.get_transaction_by_id(transaction_id)
    return transaction, HTTPStatus.OK
