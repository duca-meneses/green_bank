from uuid import UUID

from flask_jwt_extended import jwt_required
from sqlalchemy import select
from sqlalchemy.orm import Session

from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.schemas.transaction_schema import TransactionSchema
from green_bank.domain.model.transaction import Transaction
from green_bank.domain.model.user import User, UserType
from green_bank.infra.database import get_session


class TransactionService:
    def __init__(self, session: Session = None):
        self.session = session or get_session().__enter__()

    jwt_required()
    def create_transaction(self, transaction: dict):
        '''
        Creates a transaction between a payer and a payee.
        Args:
            transaction (dict): A dictionary containing transaction details with keys:
                - 'payer' (UUID): The ID of the payer.
                - 'payee' (UUID): The ID of the payee.
                - 'value' (float): The amount to be transferred.
        Raises:
            GreenBankBasicException: If the payer has insufficient balance.
            GreenBankBasicException: If the payer is a retailer.
        Returns:
            dict: A dictionary containing the transaction details with keys:
                - 'value' (float): The amount transferred.
                - 'payer' (dict): A dictionary with the payer's details:
                    - 'id' (UUID): The ID of the payer.
                    - 'name' (str): The name of the payer.
                - 'payee' (dict): A dictionary with the payee's details:
                    - 'id' (UUID): The ID of the payee.
                    - 'name' (str): The name of the payee.
        '''

        with get_session() as session:
            payer: User = session.scalar(
                select(User).where(User.id == transaction['payer'])
            )

            payee: User = session.scalar(
                select(User).where(User.id == transaction['payee'])
            )

            if payer.wallet_balance <= transaction['value']:
                raise GreenBankBasicException('Insufficient balance')

            if payer.user_type == UserType.RETAILER:
                raise GreenBankBasicException('Retailer cannot make transactions')

            payer.wallet_balance -= transaction['value']
            payee.wallet_balance += transaction['value']

            db_transaction: Transaction = Transaction(
                amount=transaction['value'],
                sender_id=payer.id,
                receiver_id=payee.id
            )

            session.add(db_transaction)
            session.commit()
            session.refresh(db_transaction)

            transaction_schema = TransactionSchema()
            return transaction_schema.dump(
                {
                    "value": db_transaction.amount,
                    "payer": {
                        "id": payer.id,
                        "name": payer.name
                    },
                    "payee": {
                        "id": payee.id,
                        "name": payee.name
                    },
                    "created": db_transaction.created
                }
            )

    jwt_required()
    def list_transactions(self, payer_name: str = None, payee_name: str = None):
        '''
        Fetches all transactions from the database.
        Returns:
            list: A list of dictionaries containing transaction details with keys:
                - 'value' (float): The amount transferred.
                - 'payer' (dict): A dictionary with the payer's details:
                    - 'id' (UUID): The ID of the payer.
                    - 'name' (str): The name of the payer.
                - 'payee' (dict): A dictionary with the payee's details:
                    - 'id' (UUID): The ID of the payee.
                    - 'name' (str): The name of the payee.
        '''
        query = select(Transaction)

        if payer_name:
            query = query.filter(Transaction.sender.has(name=payer_name))

        if payee_name:
            query = query.filter(Transaction.receiver.has(name=payee_name))

        transactions = self.session.scalars(query)
        transaction_schema = TransactionSchema(many=True)

        list_schema = [
            {
                "value": transaction.amount,
                "payer": {
                    "id": transaction.sender.id,
                    "name": transaction.sender.name
                },
                "payee": {
                    "id": transaction.receiver.id,
                    "name": transaction.receiver.name
                },
                "created": transaction.created
            }
            for transaction in transactions
        ]

        return transaction_schema.dump(list_schema)

    jwt_required()
    def get_transaction_by_id(self, transaction_id: UUID):
        '''
        Fetches a transaction from the database.
        Args:
            transaction_id (UUID): The ID of the transaction to be fetched.
        Returns:
            dict: A dictionary containing the transaction details with keys:
                - 'value' (float): The amount transferred.
                - 'payer' (dict): A dictionary with the payer's details:
                    - 'id' (UUID): The ID of the payer.
                    - 'name' (str): The name of the payer.
                - 'payee' (dict): A dictionary with the payee's details:
                    - 'id' (UUID): The ID of the payee.
                    - 'name' (str): The name of the payee.
        '''
        transaction = self.session.scalar(
            select(Transaction).where(Transaction.id == transaction_id)
        )

        transaction_schema = TransactionSchema()
        return transaction_schema.dump(
            {
                "value": transaction.amount,
                "payer": {
                    "id": transaction.sender.id,
                    "name": transaction.sender.name
                },
                "payee": {
                    "id": transaction.receiver.id,
                    "name": transaction.receiver.name
                },
                "created": transaction.created
            }
        )



transaction_service = TransactionService()
