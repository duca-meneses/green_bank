from http import HTTPStatus

from flask_jwt_extended import create_access_token
from sqlalchemy import select
from sqlalchemy.orm import Session

from green_bank.application.errors.green_bank_exception import GreenBankBasicException
from green_bank.application.schemas.auth_schema import TokenSchema
from green_bank.domain.model.user import User
from green_bank.infra.database import get_session
from green_bank.infra.security import bcrypt


class AuthService:
    def __init__(self, session: Session = get_session()):
        self.session = next(session)


    def login(self, username, password) -> User:
        db_user = self.session.scalar(
            select(User).where(User.email == username)
        )

        if not db_user or not self.__verify_password(db_user.password, password):
            raise GreenBankBasicException(
                "Bad email or password",
                HTTPStatus.UNAUTHORIZED
            )

        access_token = create_access_token(identity=db_user.email,
                                           additional_claims={"name": db_user.name})

        token = TokenSchema().dump({"access_token": access_token})

        return token

    def change_password(self, user_id, data):
        user = self.session.scalar(
            select(User).where(User.id == user_id)
        )

        if not user:
            raise GreenBankBasicException(
                "User not found",
                HTTPStatus.NOT_FOUND
            )

        if not self.__verify_password(user.password, data["old_password"]):
            raise GreenBankBasicException(
                "Bad password",
                HTTPStatus.BAD_REQUEST
            )

        user.password = bcrypt.generate_password_hash(data["new_password"])

        self.session.commit()

    def __verify_password(self, password_hash, password_raw):
        return bcrypt.check_password_hash(password_hash, password_raw)


auth_service = AuthService()
