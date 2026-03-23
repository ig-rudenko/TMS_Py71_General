import sqlite3

from .exceptions import UniqueError
from .abstracts import AbstractStorage
from .types import User, Post


class SQLiteUserStorage(AbstractStorage):

    def __init__(self, table_name: str, db_path: str):
        self._table_name = table_name
        self._db_path = db_path

    def get_by(self, field: str, value: str | int) -> User:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self._table_name} WHERE {field}='{value}'")
            data = cursor.fetchone()
        finally:
            conn.close()

        return User(id=data[0], username=data[1], first_name=data[2], last_name=data[3], password=data[4],
                    email=data[5])

    def get_by_id(self, id_: int) -> User:
        return self.get_by('id', id_)

    def add(self, obj: User):
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"INSERT INTO {self._table_name} (username, first_name, last_name, password, email) VALUES (?, ?, ?, ?, ?)",
                (
                    getattr(obj, "username"),
                    getattr(obj, "first_name"),
                    getattr(obj, "last_name"),
                    getattr(obj, "password"),
                    getattr(obj, "email"),
                )
            )
        except sqlite3.IntegrityError as exc:
            error_msg = str(exc)
            if "UNIQUE constraint failed" in error_msg:
                raise UniqueError(error_msg) from exc
            raise
        else:
            conn.commit()
        finally:
            conn.close()

    def remove(self, id_: int) -> bool:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {self._table_name} WHERE id = {id_}")
        finally:
            conn.close()

        conn.commit()
        return True


class SQLitePortStorage(AbstractStorage):

    def __init__(self, table_name: str, db_path: str):
        self._table_name = table_name
        self._db_path = db_path

    def get_by(self, field: str, value: str | int) -> Post | None:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self._table_name} WHERE {field}='{value}'")
            data = cursor.fetchone()
        finally:
            conn.close()

        if data is None:
            return None

        return Post(id=data[0], title=data[1], content=data[2], user_id=data[3], created_at=data[4])

    def get_user_posts(self, user_id: int, search: str) -> list[Post] | None:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self._table_name} WHERE title like ? and user_id=?", (search, user_id))
            data = cursor.fetchall()
        finally:
            conn.close()

        if data is None:
            return None

        return [Post(id=row[0], title=row[1], content=row[2], user_id=row[3], created_at=row[4]) for row in data]

    def get_by_id(self, id_: int) -> Post | None:
        return self.get_by('id', id_)

    def add(self, obj: Post):
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"INSERT INTO {self._table_name} (title, content, user_id, created_at) VALUES (?, ?, ?, ?)",
                (
                    getattr(obj, "title"),
                    getattr(obj, "content"),
                    getattr(obj, "user_id"),
                    getattr(obj, "created_at"),
                )
            )
        except sqlite3.IntegrityError as exc:
            error_msg = str(exc)
            if "UNIQUE constraint failed" in error_msg:
                raise UniqueError(error_msg) from exc
            raise
        else:
            conn.commit()
        finally:
            conn.close()

    def remove(self, id_: int) -> bool:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {self._table_name} WHERE id = {id_}")
        finally:
            conn.close()

        conn.commit()
        return True
