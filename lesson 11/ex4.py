class User:
    def __init__(self, username: str, email: str, first_name: str, last_name: str):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def json(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Student(User):
    def __init__(self, username: str, email: str, first_name: str, last_name: str, group: str, phone: str):
        super().__init__(username, email, first_name, last_name)
        self.group = group
        self.phone = phone

    def json(self) -> dict:
        json_data = super().json()
        return {
            **json_data,
            "group": self.group,
            "phone": self.phone,
        }


class Teacher(User):
    def __init__(self, username: str, email: str, first_name: str, last_name: str, phone: str, groups: list[str]):
        super().__init__(username, email, first_name, last_name)
        self.phone = phone
        self.groups = groups

    def json(self) -> dict:
        json_data = super().json()
        return {
            **json_data,
            "groups": self.groups,
            "phone": self.phone,
        }


user_1 = User("user123","user123@gmail.com", "Ivan","Ivanovich")
user_2 = Student("alice123","alice123@gmail.com", "Alice","Ivanovna", "Py71", "+9827-389-17-31")


print(user_1.json())
print(user_2.json())