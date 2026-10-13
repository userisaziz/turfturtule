import uuid

from sqlalchemy import Enum, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.enums import TurfSports
from core.database import Base


class Ground(Base):
    __tablename__ = "grounds"
    id:Mapped[uuid.UUID]=mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    turf_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("turfs.id"), nullable=False)
    sports:Mapped[TurfSports]=mapped_column(Enum(TurfSports, native_enum=False), nullable=False)
