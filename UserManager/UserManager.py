import json
from User import User

class UserManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = []
        self.load_users()  

    def save_users(self):
        with open(self.filename, 'w') as f:
            json.dump([user.__dict__ for user in self.users], f, indent=2)

    def load_users(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.users = [User(**user_data) for user_data in data]
        except FileNotFoundError:
            self.users = []

    def get_user_by_id(self, user_id):
        return next((user for user in self.users if user.id == user_id), None)

    def get_user_by_username(self, username):
        return next((user for user in self.users if user.username == username), None)

    def get_users_by_status(self, status):
        return [user for user in self.users if user.status == status]

    def get_all_users(self):
        return self.users

    def add_user(self, user):
        self.users.append(user)
        self.save_users()  

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            self.save_users()
            return True
        return False