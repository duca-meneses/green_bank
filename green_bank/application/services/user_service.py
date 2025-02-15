from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.orm import Session

from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.schemas.user_schema import UpdateUserSchema, UserSchema
from green_bank.application.validators.document_validate import (
    validar_cnpj,
    validar_cpf,
)
from green_bank.application.validators.email_validate import email_validate
from green_bank.domain.model.user import DocumentType, User, UserType
from green_bank.infra.database import get_session
from green_bank.infra.security import bcrypt


class UserService():
    def __init__(self, session: Session= None):
        self.session = session or get_session().__enter__()


    def create_user(self, user):

        db_user = self.session.scalar(
            select(User).where(
                (User.email == user['email']) |
                (User.document_number == user["document_number"])
            )
        )
        if db_user:
            raise GreenBankBasicException('User already exists', HTTPStatus.CONFLICT)

        if not validar_cpf(
            user['document_number']) | validar_cnpj(user['document_number']
        ):
            raise GreenBankBasicException('Invalid document number')


        db_user = User(
            name=user['name'],
            email=user['email'],
            document_number=user['document_number'],
            password=bcrypt.generate_password_hash(user['password']),
            wallet_balance=user['wallet_balance']
        )
        validate_user_type = self.__is_retailer_or_customer(user['document_number'])
        db_user.user_type, db_user.document_type = validate_user_type

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        user_schema = UserSchema()
        user = user_schema.dump(db_user)

        return user


    def get_users(self,):
        db_users = self.session.scalars(select(User))
        users_schema = UserSchema(many=True)
        users = users_schema.dump(db_users)
        return users

    def get_user(self, user_id):
        db_user = self.session.scalar(select(User).where(User.id == user_id))
        if not db_user:
            raise GreenBankBasicException('User not found', HTTPStatus.NOT_FOUND)
        user_schema = UserSchema()
        user = user_schema.dump(db_user)

        return user

    def update_user(self, user_id, user):
        db_user = self.session.scalar(select(User).where(User.id == user_id))

        if not db_user:
            raise GreenBankBasicException('User not found', HTTPStatus.NOT_FOUND)

        db_user.name = user['name']
        db_user.email = user['email']

        self.session.commit()
        self.session.refresh(db_user)

        user_schema = UpdateUserSchema()
        user = user_schema.dump(db_user)

        return user


    def delete_user(self, user_id):
        db_user = self.session.scalar(select(User).where(User.id == user_id))
        if not db_user:
            raise GreenBankBasicException('User not found', HTTPStatus.NOT_FOUND)
        self.session.delete(db_user)
        self.session.commit()


    def __is_retailer_or_customer(self, document_number):
        if validar_cnpj(document_number):
            return (UserType.RETAILER, DocumentType.CNPJ)
        if validar_cpf(document_number):
            return (UserType.CUSTOMER, DocumentType.CPF)

    def __is_email_valid(self, email):
        if len(email) >= 10 and email_validate(email):  # noqa: PLR2004
            return True


user_service = UserService()
