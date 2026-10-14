import uuid

from pydantic import BaseModel, ConfigDict

from app.utils.enums import TurfSports


class GroundCreate(BaseModel):
    name: str
    turf_id: uuid.UUID
    sports: list[TurfSports]


class GroundRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    turf_id: uuid.UUID
    sports: list[TurfSports]
