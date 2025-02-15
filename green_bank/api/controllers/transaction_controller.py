from http import HTTPStatus
from uuid import UUID

from flask import request
from flask.blueprints import Blueprint
from marshmallow import ValidationError

from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.schemas.transaction_schema import CreateTransactionSchema
from green_bank.application.services.transaction_service import transaction_service

transaction = Blueprint('transaction', __name__, url_prefix='/transactions')


@transaction.route('/transfer', methods=['POST'])
def create_transfer():
    transaction_schema = CreateTransactionSchema()
    try:
        transaction = transaction_schema.load(request.json)
    except ValidationError as error:
        raise GreenBankBasicException(error.messages, HTTPStatus.UNPROCESSABLE_ENTITY)
    transaction_response = transaction_service.create_transaction(transaction)
    return transaction_response, HTTPStatus.CREATED

@transaction.route('/', methods=['GET'])
def get_transactions():
    payer_name = request.args.get('payer_name')
    payee_name = request.args.get('payee_name')
    transactions = transaction_service.list_transactions(payer_name, payee_name)
    return {'transactions': transactions}, HTTPStatus.OK

@transaction.route('/<uuid:transaction_id>', methods=['GET'])
def get_transaction(transaction_id: UUID):
    transaction = transaction_service.get_transaction(transaction_id)
    return transaction, HTTPStatus.OK
