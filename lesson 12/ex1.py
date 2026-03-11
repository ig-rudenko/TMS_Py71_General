import json
import pathlib
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class User:
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

    def json(self):
        return self.__dict__


@dataclass(kw_only=True)
class Post:
    id: int
    title: str
    author: int
    content: str
    created_at: datetime = field(default_factory=datetime.now)

    def json(self):
        return {
            **self.__dict__,
            "created_at": self.created_at.isoformat()
        }


class StorageError(Exception): ...

class ObjectNotFound(StorageError): ...


class Storage:

    def __init__(self, storage_dir: pathlib.Path, bucket_name: str):
        self.bucket_name = bucket_name
        self._bucket_file = storage_dir / (self.bucket_name + ".json")
        self._bucket_file.touch()
        self._data: list = []
        self._load_data()

    def _load_data(self):
        with open(self._bucket_file, "r", encoding="utf-8") as f:
            try:
                self._data = json.load(f)
            except json.decoder.JSONDecodeError:
                pass

    def _save_data(self):
        with open(self._bucket_file, "w", encoding="utf-8") as f:
            json_data = [obj.json() for obj in self._data]
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            print("save")

    @property
    def data(self):
        return self._data

    def get_by_id(self, id_: int):
        print("get_by_id", self._data)
        for data in self._data:
            print("data line", data)
            if data.id == id_:
                return data
        raise ObjectNotFound(f"Object Not Found by id {id_!r}")

    def add_object(self, obj):
        try:
            self.get_by_id(obj.id)
        except ObjectNotFound:
            print("ObjectNotFound")
            self._data.append(obj)
            self._save_data()

    def remove_object_by_id(self, id_: int) -> bool:
        for data in self._data:
            if data["id"] == id_:
                self._data.remove(data)
                self._save_data()
                return True
        return False


BASE_DIR = pathlib.Path(__file__).parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

user_storage = Storage(STORAGE_DIR, "users")

user1 = User(id=1, username="user123", email="user123@gmail.com", first_name="Ivan", last_name="Ivanovich", password="12345")

print("add_object")
user_storage.add_object(user1)
