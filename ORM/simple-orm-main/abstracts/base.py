from dataclasses import dataclass, field, asdict
from typing import Self
from uuid import uuid4
import json
from enum import Enum

@dataclass
class BaseModel:
    _id: str = field(default_factory=lambda: str(uuid4()), init=False)

    @property
    def id(self) -> str:
        return self._id

    def to_dict(self) -> dict:
        data = asdict(self)
        data["id"] = self.id
        for k, v in data.items():
            if isinstance(v, Enum):
                data[k] = v.value
        return data

    @classmethod
    def from_dict(cls, dict_data: dict) -> Self:
        id_value = dict_data.pop("id", None)
        obj = cls.__new__(cls)  # bypass dataclass __init__

        for field_name, field_type in getattr(cls, "__annotations__", {}).items():
            if field_name in dict_data:
                value = dict_data[field_name]
                if isinstance(field_type, type) and issubclass(field_type, Enum):
                    try:
                        dict_data[field_name] = field_type(value)
                    except ValueError:
                        dict_data[field_name] = list(field_type)[0]

        for k, v in dict_data.items():
            setattr(obj, k, v)

        setattr(obj, "_id", id_value or str(uuid4()))
        return obj

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, json_value: str) -> Self:
        return cls.from_dict(json.loads(json_value))

    def __repr__(self) -> str:
        return self.to_json()
