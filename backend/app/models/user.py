
import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Enum, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.enums import UserRole


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID]=mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    phone: Mapped[str]=mapped_column(String(15), unique=True, index=True)
    name: Mapped[str | None]=mapped_column(String(120))
    email: Mapped[str | None]=mapped_column(String(255))
    roles: Mapped[list[UserRole]] = mapped_column(
        ARRAY(Enum(UserRole, native_enum=False)),
        nullable=False,
        server_default=text("'{}'"),
    )
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
