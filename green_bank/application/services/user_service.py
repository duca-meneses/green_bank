from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import Session
from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.validators.document_validate import validar_cnpj, validar_cpf
from green_bank.application.validators.email_validate import email_validate
from green_bank.domain.model.user import DocumentType, User, UserType
from green_bank.infra.database import get_session


class UserService():
    def __init__(self, session: Session=get_session()):
        self.session = next(session)

    
    def create_user(self, user):

        if not self.__is_email_valid(user['email']):
            raise GreenBankBasicException('Invalid email', HTTPStatus.BAD_REQUEST)
        
        db_user = self.session.scalar(
            select(User).where(
                (User.email == user['email']) | 
                (User.document_number == user["document_number"])
            )   
        )
        if db_user:
            raise GreenBankBasicException('User already exists', HTTPStatus.CONFLICT)

        if not validar_cpf(user['document_number']) | validar_cnpj(user['document_number']):
            raise GreenBankBasicException('Invalid document number')

        
        db_user = User(
            name=user['name'],
            email=user['email'],
            document_number=user['document_number'],
            password=user['password'],
            wallet_balance=user['wallet_balance']        
        )
        db_user.user_type, db_user.document_type = self.__is_retailer_or_customer(user['document_number'])

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return db_user
                

    def get_users(self,):
        db_users = self.session.scalars(select(User))
        users = [user for user in db_users]
        return users

    def get_user(self, user_id):
        db_user = self.session.scalar(select(User).where(User.id == user_id))
        if not db_user:
            raise GreenBankBasicException('User not found', HTTPStatus.NOT_FOUND)

        print(db_user)
        
        return db_user

    def update_user(self, user_id, user):
        db_user = self.session.scalar(select(User).where(User.id == user_id))

        if not db_user:
            raise GreenBankBasicException('User not found', HTTPStatus.NOT_FOUND)

        db_user.name = user['name']
        db_user.email = user['email']

        self.session.commit()
        self.session.refresh(db_user)

        return db_user
        

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
        if len(email) >= 10 and email_validate(email):
            return True
        

user_service = UserService()