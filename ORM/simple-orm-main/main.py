from models.user import User
from models.post import Post

def main():
    # Создаем пользователей
    if not User.objects.get():
        User.objects.add([User(username="alice")])
        User.objects.add([User(username="bob")])

    for u in User.objects.get():
        print(f"User: {u.username}, Status: {u.status.name}")

    # Создаем пост
    if not Post.objects.get():
        Post.objects.add([Post(title="Hello", description="Short", text="Full text")])

    for p in Post.objects.get():
        print(f"Post: {p.title}, Status: {p.status.name}")

if __name__ == "__main__":
    main()
