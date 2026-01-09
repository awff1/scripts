from enum import Enum

class EntityManager:
    def __init__(self, model_cls):
        self.model_cls = model_cls
        self._storage = []

    def create(self, **kwargs):
        obj = self.model_cls(**kwargs)
        self.save(obj)
        return obj

    def save(self, obj):
        if obj not in self._storage:
            self._storage.append(obj)

    def all(self):
        return list(self._storage)
    

class ModelMeta(type):
    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)
        if name != "Model":
            cls.objects = EntityManager(cls)
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
    def __init__(self, username, status=UserStatus.ACTIVE):
        self.username = username
        self.status = status

    def __repr__(self):
        return f"<User {self.username} ({self.status.value})>"

class Post(Model):
    def __init__(self, title, description, text, status=PostStatus.DRAFT):
        self.title = title
        self.description = description
        self.text = text
        self.status = status

    def __repr__(self):
        return f"<Post {self.title} ({self.status.value})>"

# User
user1 = User.objects.create(username="alice")
user2 = User(username="bob", status=UserStatus.BLOCKED)
user2.save()

print(User.objects.all())

# Post
post1 = Post.objects.create(
    title="Hello",
    description="Intro",
    text="Hello world",
    status=PostStatus.PUBLISHED
)

post2 = Post(
    title="Draft post",
    description="Draft",
    text="...",
)
post2.save()

print(Post.objects.all())
