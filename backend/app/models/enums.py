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
