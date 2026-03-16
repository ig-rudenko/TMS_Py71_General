from .abstracts import AbstractStorage, AbstractObject


TYPES_STORAGES_MAP: dict[type[AbstractObject], type[AbstractStorage]] = {}
