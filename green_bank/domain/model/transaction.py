import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from green_bank.domain.model.entity import Base, table_registry


@table_registry.mapped_as_dataclass
class Transaction(Base):
    __tablename__ = 'transactions'

    sender_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    receiver_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id'), nullable=False
        )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False,
    )

    sender = relationship('User', foreign_keys=[sender_id])
    receiver = relationship('User', foreign_keys=[receiver_id])

    def __repr__(self):

        sender = self.sender.name
        receiver = self.receiver.name
        return f'<Transaction {self.id} {sender} {receiver} {self.amount}>'
