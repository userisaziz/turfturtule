import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import BookingStatus


class BookingCreate(BaseModel):
    ground_id: uuid.UUID
    date: date
    start_time: datetime
    end_time: datetime
    total_amount: int


class BookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    ground_id: uuid.UUID
    user_id: uuid.UUID
    date: date
    start_time: datetime
    end_time: datetime
    total_amount: int
    status: BookingStatus
    created_at: datetime
    updated_at: datetime
