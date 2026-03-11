class User:
    """Объект пользователя"""

    def __init__(self, username: str, email: str, first_name: str, last_name: str):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.__password = "1231231231"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.get_full_name()

    def __len__(self) -> int:
        return len(self.get_full_name())

    def __lt__(self, other):
        if isinstance(other, User):
            return self.get_full_name() < other.get_full_name()
        raise TypeError(f"Нельзя сравнивать User с {type(other)}")


user_1 = User("user123", "user123@gmail.com", "Ivan", "Ivanovich")
user_2 = User("alice123", "alice123@gmail.com", "Alice", "Ivanovna")

attrs = []
methods = []
for attr in user_1.__dir__():
    if callable(getattr(user_1, attr)):
        methods.append(attr)
    else:
        attrs.append(attr)

for method in sorted(methods):
    print("Метод:", method, getattr(user_1, method))

for attr in sorted(attrs):
    print("Атрибут:", attr, getattr(user_1, attr))

print("-" * 200)

print(user_2 < 123)
