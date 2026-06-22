from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query

from ..schemas.general import GeneralSchema

router = APIRouter(prefix="/general", tags=["general"])


class A:
    def __init__(self, hello: str, key1: int, key2: str):
        self.hello = hello
        self.key1 = key1
        self.key2 = key2


@router.get("/", response_model=GeneralSchema)
async def handler1(search: Annotated[str, Query()] = "", page: Annotated[int, Query(gt=0)] = 1):
    return A(search, page, "secret")


@router.post("/", status_code=201)
async def handler2(data: GeneralSchema):
    print(data)
