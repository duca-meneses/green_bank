
from flask.blueprints import Blueprint

from green_bank.api.spec import api_key_scheme, spec
from green_bank.application.schemas.auth_schema import (
    CreateLoginSchema,
    PasswordChangeSchema,
    TokenSchema,
)
from green_bank.application.schemas.error_schema import ErrorSchema
from green_bank.application.schemas.message import HealthCheckSchema, MessageSchema
from green_bank.application.schemas.transaction_schema import (
    CreateTransactionSchema,
    TransactionSchema,
)
from green_bank.application.schemas.user_schema import (
    CreateUpdateUserSchema,
    CreateUserSchema,
    UpdateUserSchema,
    UserSchema,
    listUserSchema,
)

from .controllers.auth_controller import bp as auth
from .controllers.health_check import hc
from .controllers.transaction_controller import transaction
from .controllers.user_controller import app as user

api_router = Blueprint('api', __name__)
api_router.register_blueprint(hc)
api_router.register_blueprint(user)
api_router.register_blueprint(auth)
api_router.register_blueprint(transaction)



spec.components.security_scheme('APIKeyAuth', api_key_scheme)
spec.components.schema('ErrorSchema', schema=ErrorSchema)
spec.components.schema('UserSchema', schema=UserSchema)
spec.components.schema('ListUserSchema', schema=listUserSchema)
spec.components.schema('CreateUserSchema', schema=CreateUserSchema)
spec.components.schema('CreateUpdateUserSchema', schema=CreateUpdateUserSchema)
spec.components.schema('UpdateUserSchema', schema=UpdateUserSchema)

spec.components.schema('CreateLoginSchema', schema=CreateLoginSchema)
spec.components.schema('TokenSchema', schema=TokenSchema)
spec.components.schema('PasswordChangeSchema', schema=PasswordChangeSchema)

spec.components.schema('TransactionSchema', schema=TransactionSchema)
spec.components.schema('CreateTransactionSchema', schema=CreateTransactionSchema)
spec.components.schema('MessageSchema', schema=MessageSchema)

spec.components.schema('HealthCheckSchema', schema=HealthCheckSchema)
