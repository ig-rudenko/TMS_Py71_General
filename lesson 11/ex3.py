import random
import string


class User:
    def __init__(self, username: str, email: str, first_name: str, last_name: str, password: str = ""):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self._password = password

        if not self._password:
            self._generate_password()

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value) < 12:
            raise ValueError("Password must be at least 12 characters")
        self._password = value

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def _generate_password(self, max_length: int = 12):
        passwd = ""
        for i in range(max_length):
            passwd += random.choice(string.ascii_letters + string.digits)
        self._password = passwd

    def json(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


user_1 = User("user123", "user123@gmail.com", "Ivan", "Ivanovich")
user_2 = User("alice123", "alice123@gmail.com", "Alice", "Ivanovna")

print(user_1.full_name)

print(user_1.full_name)
