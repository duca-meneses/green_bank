from http import HTTPStatus
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from sqlalchemy.orm import Session

from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.domain.model.user import User
from green_bank.infra.database import get_session



class AuthService:
    def __init__(self, session: Session = get_session()):
        self.session = next(session)


    def login(self, username, password) -> User:
        db_user = self.session.scalar(
            select(User).where(
                (User.email == username) & (User.password == password)
            )
        )

        if not db_user:
            raise GreenBankBasicException("Bad email or password", HTTPStatus.UNAUTHORIZED)

        access_token = create_access_token(identity=db_user.email)

        return access_token


auth_service = AuthService()