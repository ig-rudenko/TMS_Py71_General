def get_new_username(first_name: str, last_name: str) -> str:
    return f"{first_name}_{last_name}".lower()


def get_user_names(username: str) -> tuple[str, str]:  # 'ivan_ivanov'
    parts = username.split("_")  # ['ivan', 'ivanov']
    first_name = parts[0].title()  # 'Ivan'
    last_name = parts[1].title()  # 'Ivanov'

    return first_name, last_name  # ('Ivan', 'Ivanov')


user_1 = {
    "username": "ivan",
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "email": "ivan@mail.com",
    "age": 25,
    "address": {
        "city": "New York",
        "street": "1st"
    }
}

print(user_1)

user_1["username"] = get_new_username(user_1["first_name"], user_1["last_name"])

print(user_1)

first_name, last_name = get_user_names(user_1["username"])

print(first_name, last_name, type(first_name), type(last_name))
