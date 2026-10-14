import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import UserRole


class UserCreate(BaseModel):
    phone: str = Field(min_length=10, max_length=15)
    name: str | None = None
    email: str | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    phone: str
    name: str | None
    email: str | None
    roles: list[UserRole]
    created_at: datetime