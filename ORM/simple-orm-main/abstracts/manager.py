from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar
from abstracts.base import BaseModel

T = TypeVar("T", bound=BaseModel)

class AbstractEntityManager(ABC):

    def __init__(self, cls: type[T]):
        self._cls = cls

    @abstractmethod
    def add(self, entities: List[T]) -> List[T]:
        pass

    @abstractmethod
    def get(self, criteria: Optional[dict] = None) -> List[T]:
        pass

    @abstractmethod
    def update(self, criteria: dict, changes: dict) -> List[T]:
        pass

    @abstractmethod
    def delete(self, criteria: dict) -> List[T]:
        pass

    @abstractmethod
    def save(self):
        pass
