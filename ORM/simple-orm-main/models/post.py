from dataclasses import dataclass
from enum import Enum
from abstracts.base import BaseModel
from abstracts.meta import Meta

class PostStatus(Enum):
    CREATED = 0
    PUBLISHED = 1
    DELETED = 2

@dataclass
class Post(BaseModel, metaclass=Meta):
    title: str
    description: str
    text: str
    status: PostStatus = PostStatus.CREATED
