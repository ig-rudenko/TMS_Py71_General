import json
import pathlib
from abc import ABC, abstractmethod
from typing import Self

from .exceptions import ObjectNotFound


class AbstractObject(ABC):
    id: int

    @abstractmethod
    def json(self) -> dict: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_data: dict) -> Self: ...


class AbstractStorage:
    obj_class: type[AbstractObject]

    def __init__(self, storage_dir: pathlib.Path):
        self._bucket_file = storage_dir / (self.obj_class.__name__.lower() + "s" + ".json")
        self._bucket_file.touch()
        self._data: list[AbstractObject] = []
        self._load_data()

    def _load_data(self):
        with open(self._bucket_file, "r", encoding="utf-8") as f:
            try:
                json_data: list[dict] = json.load(f)
                self._data = [self.obj_class.from_dict(obj) for obj in json_data]
                print("✅ Load from file")
            except json.decoder.JSONDecodeError:
                pass

    def _save_data(self):
        with open(self._bucket_file, "w", encoding="utf-8") as f:
            json_data: list[dict] = [obj.json() for obj in self._data]
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            print("✅ Save to file")

    @property
    def data(self):
        return self._data

    def get_by_id(self, id_: int) -> AbstractObject:
        for data in self._data:
            if data.id == id_:
                return data
        raise ObjectNotFound(f"Object Not Found by id {id_!r}")

    def add_object(self, obj: AbstractObject):
        try:
            self.get_by_id(obj.id)
        except ObjectNotFound:
            print("❌ ObjectNotFound")
            self._data.append(obj)
            self._save_data()

    def remove_object_by_id(self, id_: int) -> bool:
        for data in self._data:
            if data["id"] == id_:
                self._data.remove(data)
                self._save_data()
                return True
        return False

