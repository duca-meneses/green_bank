from decimal import Decimal
from enum import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped , mapped_column

from green_bank.domain.model.entity import Base, table_registry


class UserType(str, Enum):
    CUSTOMER = 'customer'
    RETAILER = 'retailer'

class DocumentType(str, Enum):
    CPF = 'cpf'
    CNPJ = 'cnpj'

@table_registry.mapped_as_dataclass
class User(Base):
    __tablename__ = 'users'
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    document_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    user_type: Mapped[UserType] = mapped_column(nullable=False, index=True)
    document_type: Mapped[DocumentType] = mapped_column(nullable=False, index=True)
    wallet_balance: Mapped[Decimal] = mapped_column(nullable=True, default=0.00)
