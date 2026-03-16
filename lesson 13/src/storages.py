from .abstracts import AbstractObject, AbstractStorage
from .types import User, Post
from .helper import TYPES_STORAGES_MAP

class UserStorage(AbstractStorage):
    obj_class: type[AbstractObject] = User


class PostStorage(AbstractStorage):
    obj_class: type[AbstractObject] = Post


TYPES_STORAGES_MAP[User] = UserStorage
TYPES_STORAGES_MAP[Post] = PostStorage
