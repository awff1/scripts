from User import User
from UserManager import UserManager


def main():
    print("=== ИНИЦИАЛИЗАЦИЯ МЕНЕДЖЕРА ===")
    manager = UserManager("users.json")

    print("\n=== ОЧИСТКА ФАЙЛА (для чистого теста) ===")
    manager.users = []
    manager.save_users()

    print("\n=== ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ===")
    user1 = User(id=1, username="alice", status="active")
    user2 = User(id=2, username="bob", status="blocked")
    user3 = User(id=3, username="charlie", status="active")

    manager.add_user(user1)
    manager.add_user(user2)
    manager.add_user(user3)

    print("\n=== ВСЕ ПОЛЬЗОВАТЕЛИ ===")
    for user in manager.get_all_users():
        print(user)

    print("\n=== ПОИСК ПО ID ===")
    print(manager.get_user_by_id(2))     # bob
    print(manager.get_user_by_id(99))    # None

    print("\n=== ПОИСК ПО USERNAME ===")
    print(manager.get_user_by_username("alice"))
    print(manager.get_user_by_username("unknown"))

    print("\n=== ФИЛЬТР ПО STATUS ===")
    active_users = manager.get_users_by_status("active")
    for user in active_users:
        print(user)

    print("\n=== УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ ===")
    result = manager.delete_user(2)
    print("Удалён:", result)

    print("\n=== ПОЛЬЗОВАТЕЛИ ПОСЛЕ УДАЛЕНИЯ ===")
    for user in manager.get_all_users():
        print(user)

    print("\n=== ПРОВЕРКА СОХРАНЕНИЯ И ЗАГРУЗКИ ===")
    new_manager = UserManager("users.json")
    for user in new_manager.get_all_users():
        print(user)


if __name__ == "__main__":
    main()
