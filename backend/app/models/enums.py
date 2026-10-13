import enum


class TurfStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    rejected = "rejected"


class TurfSports(str, enum.Enum):
    cricket = "cricket"
    football = "football"
    basketball = "basketball"
    tennis = "tennis"
    volleyball = "volleyball"

class TimeOfDay(str, enum.Enum):
    day = "day"
    night = "night"

class Status(str, enum.Enum):
    active = "active"
    pending = "pending"
    rejected = "rejected"

class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class PaymentMethod(str, enum.Enum):
    upi = "upi"
    card = "card"
    cash = "cash"

class PaymentStatus(str, enum.Enum):
    initiated = "initiated"
    success = "success"
    failed = "failed"
    refunded = "refunded"