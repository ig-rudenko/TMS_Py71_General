users = [
    {
        "username": "user2",
    },
    {
        "username": "user1",
    },
    {
        "username": "user3",
    },
]


def func(obj: dict) -> str:
    return obj.get("username", "")

# Аналог
# lambda obj: obj.get("username", "")

print(users)

users_sorted = sorted(users, key=lambda obj: obj.get("username", ""))
print(users_sorted)
