import json
from pathlib import Path
from typing import List, Optional, TypeVar
from abstracts.base import BaseModel
from abstracts.manager import AbstractEntityManager
import os

T = TypeVar("T", bound=BaseModel)

class JsonEntityManager(AbstractEntityManager):
    """JSON entity manager"""

    def __init__(self, cls: type[T]):
        self._cls = cls
        self.__folder = Path(os.getenv("JSON_DATA_FOLDER", "data"))
        self.__folder.mkdir(exist_ok=True, parents=True)
        self._filename = self.__folder / f"{cls.__name__}.json"
        self.__entities: List[T] = []
        self.load()

    def load(self) -> None:
        if not self._filename.exists():
            self.__entities = []
            return
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    self.__entities = [self._cls.from_dict(d) for d in data]
                else:
                    self.__entities = []
        except json.JSONDecodeError:
            self.__entities = []

    def save(self):
        self._filename.parent.mkdir(exist_ok=True, parents=True)
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.__entities], f, ensure_ascii=False, indent=2)

    def add(self, entities: List[T]) -> List[T]:
        self.__entities.extend(entities)
        self.save()
        return entities

    def get(self, criteria: Optional[dict] = None) -> List[T]:
        if not criteria:
            return self.__entities.copy()
        return [e for e in self.__entities if all(getattr(e, k, None) == v for k, v in criteria.items())]

    def update(self, criteria: dict, changes: dict) -> List[T]:
        objs = self.get(criteria)
        for obj in objs:
            for k, v in changes.items():
                setattr(obj, k, v)
        self.save()
        return objs

    def delete(self, criteria: dict) -> List[T]:
        objs = self.get(criteria)
        self.__entities = [e for e in self.__entities if e not in objs]
        self.save()
        return objs
