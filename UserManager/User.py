class User:
    def __init__(self, id, username, status, **kwargs):
        self.id = id
        self.username = username
        self.status = status


    def __str__(self):
        return f"User(id={self.id}, username='{self.username}', status='{self.status}')"