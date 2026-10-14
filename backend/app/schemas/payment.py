import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    booking_id: uuid.UUID
    amount: int
    payment_method: PaymentMethod


class PaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    booking_id: uuid.UUID
    user_id: uuid.UUID
    payment_method: PaymentMethod
    status: PaymentStatus
    amount: int
    gateway_reference: str | None
    created_at: datetime
