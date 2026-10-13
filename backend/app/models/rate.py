import uuid

from sqlalchemy import Enum, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import TimeOfDay


class Rate(Base):
    __tablename__ = "rates"

    __table_args__ = (UniqueConstraint("ground_id", "time_of_day"),)

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    ground_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("grounds.id"), nullable=False)
    time_of_day: Mapped[TimeOfDay] = mapped_column(
        Enum(TimeOfDay, native_enum=False), nullable=False
    )
    weekday_price: Mapped[int] = mapped_column(nullable=False)
    weekend_price: Mapped[int] = mapped_column(nullable=False)
