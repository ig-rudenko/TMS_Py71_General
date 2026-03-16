import pathlib

from src.types import User

BASE_DIR = pathlib.Path(__file__).parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

user_storage = User.get_storage_class()(STORAGE_DIR)
post_storage = User.get_storage_class()(STORAGE_DIR)

user1 = User(id=1, username="user123", email="user123@gmail.com", first_name="Ivan", last_name="Ivanovich", password="12345")
user2 = User(id=2, username="user123", email="user123@gmail.com", first_name="Ivan", last_name="Ivanovich", password="12345")

user_storage.add_object(user1)
user_storage.add_object(user2)

print(user_storage.data)

print(User.get_storage_class())