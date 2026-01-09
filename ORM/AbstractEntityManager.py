from abc import ABC, abstractmethod
import sqlite3
import json
from pathlib import Path
import os
from dotenv import load_dotenv
from enum import Enum


class AbstractEntityManager(ABC):
    def __init__(self, model_cls):
        self.model_cls = model_cls

    @abstractmethod
    def create(self, **kwargs):
        ...

    @abstractmethod
    def save(self, obj):
        ...

    @abstractmethod
    def all(self):
        ...





class JsonEntityManager(AbstractEntityManager):
    def __init__(self, model_cls, base_path="data"):
        super().__init__(model_cls)
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.file_path = self.base_path / f"{model_cls.__name__.lower()}.json"

        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _load(self):
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _save(self, data):
        self.file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def create(self, **kwargs):
        obj = self.model_cls(**kwargs)
        self.save(obj)
        return obj

    def save(self, obj):
        data = self._load()
        data.append(obj.__dict__)
        self._save(data)

    def all(self):
        return [
            self.model_cls(**item)
            for item in self._load()
        ]




class SqliteEntityManager(AbstractEntityManager):
    def __init__(self, model_cls, db_name="db.sqlite3"):
        super().__init__(model_cls)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table = model_cls.__name__.lower()

        self._create_table()

    def _create_table(self):
        fields = ", ".join(
            f"{name} TEXT"
            for name in self.model_cls.__annotations__
        )

        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} ({fields})"
        )
        self.conn.commit()

    def create(self, **kwargs):
        obj = self.model_cls(**kwargs)
        self.save(obj)
        return obj

    def save(self, obj):
        fields = obj.__dict__
        columns = ", ".join(fields.keys())
        placeholders = ", ".join("?" for _ in fields)

        self.cursor.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})",
            tuple(map(str, fields.values()))
        )
        self.conn.commit()

    def all(self):
        self.cursor.execute(f"SELECT * FROM {self.table}")
        rows = self.cursor.fetchall()

        return [
            self.model_cls(**dict(zip(self.model_cls.__annotations__, row)))
            for row in rows
        ]




load_dotenv()


class ModelMeta(type):
    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)

        if name == "Model":
            return cls

        engine = os.getenv("ENGINE", "json")

        if engine == "sqlite":
            cls.objects = SqliteEntityManager(cls)
        else:
            cls.objects = JsonEntityManager(cls)

        return cls


class Model(metaclass=ModelMeta):
    def save(self):
        self.__class__.objects.save(self)




class UserStatus(Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class PostStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class User(Model):
    username: str
    status: str

    def __init__(self, username, status=UserStatus.ACTIVE):
        self.username = username

        if isinstance(status, UserStatus):
            self.status = status.value
        else:
            self.status = status


class Post(Model):
    title: str
    description: str
    text: str
    status: str

    def __init__(self, title, description, text, status=PostStatus.DRAFT):
        self.title = title
        self.description = description
        self.text = text

        if isinstance(status, PostStatus):
            self.status = status.value
        else:
            self.status = status



User.objects.create(username="alice")
User(username="bob", status=UserStatus.BLOCKED).save()

print(User.objects.all())

Post.objects.create(
    title="Hello",
    description="Intro",
    text="Hello world",
    status=PostStatus.PUBLISHED
)

print(Post.objects.all())
