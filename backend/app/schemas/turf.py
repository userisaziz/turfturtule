import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import TurfSports, TurfStatus


class TurfCreate(BaseModel):
    name: str
    description: str | None = None
    photos: list[str]
    city: str
    google_maps_url: str | None = None
    pincode: str
    sports: list[TurfSports]


class TurfRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    photos: list[str]
    city: str
    google_maps_url: str | None
    pincode: str
    sports: list[TurfSports]
    status: TurfStatus
    created_at: datetime
