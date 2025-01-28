from datetime import datetime
import uuid
from sqlalchemy import func, table
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()

class Base:

    id: Mapped[uuid.UUID] = mapped_column(init=False, primary_key=True, default=lambda: uuid.uuid4().bytes)
    created: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )