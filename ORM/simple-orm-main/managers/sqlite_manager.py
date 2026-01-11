import os
from sqlite3 import connect
from typing import List, Optional, TypeVar, Any
from enum import Enum
from abstracts.base import BaseModel
from abstracts.manager import AbstractEntityManager
from pathlib import Path

T = TypeVar("T", bound=BaseModel)

class SqliteEntityManager(AbstractEntityManager):
    def __init__(self, cls: type[T]):
        self._cls = cls
        self._table = cls.__name__
        db_file = os.getenv("DB_FILENAME", "data/sqlite.db")
        self._db_path = Path(db_file)
        self._db_path.parent.mkdir(exist_ok=True, parents=True)
        self._con = connect(str(self._db_path))
        self._cursor = self._con.cursor()
        self._create_table()

    def _get_fields(self) -> List[str]:
        fields = list(getattr(self._cls, "__annotations__", {}).keys())
        fields.append("_id")
        return fields

    def _create_table(self):
        columns = []
        for field in self._get_fields():
            if field == "_id":
                columns.append(f"{field} TEXT PRIMARY KEY")
            else:
                columns.append(f"{field} TEXT")
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {self._table} ({', '.join(columns)})")
        self._con.commit()

    def add(self, entities: List[T]) -> List[T]:
        for e in entities:
            values = []
            for field in self._get_fields():
                v = getattr(e, field, None)
                if isinstance(v, Enum):
                    v = v.value
                values.append(v)
            placeholders = ",".join("?" for _ in values)
            self._cursor.execute(
                f"INSERT OR REPLACE INTO {self._table} ({','.join(self._get_fields())}) VALUES ({placeholders})",
                tuple(values)
            )
        self._con.commit()
        return entities

    def get(self, criteria: Optional[dict] = None) -> List[T]:
        sql = f"SELECT * FROM {self._table}"
        params = []
        if criteria:
            conditions = []
            for k, v in criteria.items():
                conditions.append(f"{k}=?")
                if isinstance(v, Enum):
                    v = v.value
                params.append(v)
            sql += " WHERE " + " AND ".join(conditions)
        self._cursor.execute(sql, tuple(params))
        rows = self._cursor.fetchall()
        results = []
        for row in rows:
            data = {}
            for idx, field in enumerate(self._get_fields()):
                val = row[idx]
                field_type = getattr(self._cls, "__annotations__", {}).get(field)
                if isinstance(field_type, type) and issubclass(field_type, Enum):
                    val = field_type(val)
                data[field] = val
            if "_id" in data:
                data["_id"] = data.pop("_id")
            obj = self._cls.from_dict(data)
            results.append(obj)
        return results

    def update(self, criteria: dict, changes: dict) -> List[T]:
        objs = self.get(criteria)
        for obj in objs:
            for k, v in changes.items():
                setattr(obj, k, v)
            self.add([obj])
        return objs

    def delete(self, criteria: dict) -> List[T]:
        objs = self.get(criteria)
        for obj in objs:
            self._cursor.execute(f"DELETE FROM {self._table} WHERE _id=?", (obj.id,))
        self._con.commit()
        return objs

    def save(self):
        self._con.commit()
