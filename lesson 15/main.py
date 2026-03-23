from src.exceptions import UniqueError
from src.storages import SQLiteUserStorage, SQLitePortStorage
from src.types import User, Post

DATABASE_PATH = 'test.db'

user_storage = SQLiteUserStorage("users", DATABASE_PATH)
post_storage = SQLitePortStorage("posts", DATABASE_PATH)

def add_users():
    user1 = User(username="user123", email="user123@gmail.com", first_name="Ivan", last_name="Ivanovich",
                 password="4985902378")
    user2 = User(username="igor", email="igor@gmail.com", first_name="Igor", last_name="Ivanovich",
                 password="745897648597")

    users = [user1, user2]

    for user in users:
        try:
            user_storage.add(user)
        except UniqueError:
            pass

def add_posts():
    user = user_storage.get_by("username", "user123")
    try:
        post_storage.add(
            Post(
                title="Secret",
                content="my password = u3409u3j897903c459",
                user_id=user.id,
            )
        )
    except UniqueError:
        pass

    user = user_storage.get_by("username", "igor")
    try:
        post_storage.add(
            Post(
                title="Python",
                content="Beautiful Python",
                user_id=user.id,
            )
        )
    except UniqueError:
        pass


def login() -> User | None:
    username = input("Username: ")
    password = input("Password: ")

    user = user_storage.get_by("username", username)
    if user.password == password:
        print("Logged in successfully")
        return user
    else:
        print("Incorrect password")

    return None


def get_post(user: User):
    post_title = input("Post title: ")

    posts = post_storage.get_user_posts(user.id, post_title)
    for post in posts:
        print(post)


def main():
    add_users()
    add_posts()

    user = login()
    if user is None:
        exit(1)

    get_post(user)


if __name__ == "__main__":
    main()
