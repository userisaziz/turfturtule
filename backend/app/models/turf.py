import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Enum, ForeignKey, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.enums import TurfSports, TurfStatus


class Turf(Base):
    __tablename__ = "turfs"
    id: Mapped[uuid.UUID]=mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    owner_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str]
    description: Mapped[str | None]
    photos: Mapped[list[str]] = mapped_column(
        ARRAY(String(255)), nullable=False
    )
    city: Mapped[str]
    google_maps_url: Mapped[str | None]
    pincode: Mapped[str]
    sports: Mapped[list[TurfSports]] = mapped_column(
        ARRAY(Enum(TurfSports, native_enum=False)), nullable=False
    )
    status: Mapped[TurfStatus] = mapped_column(
        Enum(TurfStatus, native_enum=False),
        default=TurfStatus.draft,
        server_default=text("'draft'"),
    )
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
