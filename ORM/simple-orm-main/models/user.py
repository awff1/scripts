from dataclasses import dataclass
from enum import Enum
from abstracts.base import BaseModel
from abstracts.meta import Meta

class UserStatus(Enum):
    CREATED = 0
    CONFIRMED = 1
    BANNED = 2

@dataclass
class User(BaseModel, metaclass=Meta):
    username: str
    status: UserStatus = UserStatus.CREATED
