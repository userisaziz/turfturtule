import uuid

from pydantic import BaseModel, ConfigDict

from app.utils.enums import TimeOfDay


class RateCreate(BaseModel):
    ground_id: uuid.UUID
    time_of_day: TimeOfDay
    weekday_price: int
    weekend_price: int


class RateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    ground_id: uuid.UUID
    time_of_day: TimeOfDay
    weekday_price: int
    weekend_price: int
