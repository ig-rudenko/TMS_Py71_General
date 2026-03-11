def create_user_dict(username: str, email: str, first_name: str, last_name: str) -> dict:
    return {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }


user_1 = create_user_dict("user123","user123@gmail.com", "Ivan","Ivanovich")
user_2 = create_user_dict("alice123","alice123@gmail.com", "Alice","Ivanovna")


class UserIvan:
    username = "user123"
    email = "user123@gmail.com"
    first_name = "Ivan"
    last_name = "Ivanovich"


class UserAlice:
    username = "alice123"
    email = "alice123@gmail.com"
    first_name = "Alice"
    last_name = "Ivanovna"


def get_user_full_name_1(user):
    return f"{user.get('first_name')} {user.get('last_name')}"


def get_user_full_name_2(user):
    return f"{user.first_name} {user.last_name}"


print(get_user_full_name_1(user_1))
print(get_user_full_name_2(User))