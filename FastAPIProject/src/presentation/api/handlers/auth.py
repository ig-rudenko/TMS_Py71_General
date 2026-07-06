from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.application.users.handlers import UserApplicationHandler
from src.application.api_tokens.handlers import ApiTokenApplicationHandler
from src.domain.exceptions import DomainException, UniqueConstraintError
from ..dependencies import get_users_app_handler, get_api_tokens_app_handler
from ..schemas.auth import (
    UserSchema,
    RegisterUserSchema,
    LoginUserSchema,
    ApiTokenSchema,
)
from src.application.auth import current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserSchema)
async def register_user_api_view(
    data: RegisterUserSchema, handler: Annotated[UserApplicationHandler, Depends(get_users_app_handler)]
):
    try:
        return await handler.handle_register(username=data.username, password=data.password)
    except UniqueConstraintError as exc:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})
    except DomainException as exc:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})


@router.post("/login", response_model=ApiTokenSchema)
async def login_api_view(
    data: LoginUserSchema, handler: Annotated[ApiTokenApplicationHandler, Depends(get_api_tokens_app_handler)]
):
    try:
        return await handler.handle_create_api_token(username=data.username, password=data.password)
    except UniqueConstraintError as exc:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})
    except DomainException as exc:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})


@router.get("/myself", response_model=UserSchema)
async def get_myself_api_view(user: Annotated[UserSchema, Depends(current_user)]):
    return user
