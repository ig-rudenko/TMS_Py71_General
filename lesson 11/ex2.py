class User:
    def __init__(self, username: str, email: str, first_name: str, last_name: str):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = ""

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def json(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


user_1 = User("user123","user123@gmail.com", "Ivan","Ivanovich")
user_2 = User("alice123","alice123@gmail.com", "Alice","Ivanovna")


user_2.password = "p1i20389078"

