import uuid

from sqlalchemy import ARRAY, Enum, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import TurfSports


class Ground(Base):
    __tablename__ = "grounds"
    id:Mapped[uuid.UUID]=mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    turf_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("turfs.id"), nullable=False)
    sports: Mapped[list[TurfSports]] = mapped_column(
        ARRAY(Enum(TurfSports, native_enum=False)), nullable=False
    )
