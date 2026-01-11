from dotenv import load_dotenv
from abstracts.manager import AbstractEntityManager
from managers.json_manager import JsonEntityManager
from managers.sqlite_manager import SqliteEntityManager
import os

class Meta(type):
    """Metaclass for automatic manager assignment."""

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        load_dotenv()
        engine = os.getenv("ENGINE", "JSON").upper()
        if engine == "SQLITE":
            manager_cls = SqliteEntityManager
        else:
            manager_cls = JsonEntityManager
        cls.objects = manager_cls(cls)
