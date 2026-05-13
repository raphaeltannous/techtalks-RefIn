import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user import UserPublicAdmin, UserRegister, UsersPublicAdmin, UserUpdate
from routers.dependencies import get_admin_service
from services.admin import AdminService

router = APIRouter(
    tags=["admin-user-management"],
)


@router.get(
    "/all",
    response_model=UsersPublicAdmin,
)
def get_all(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    offset: int = 0,
    limit: int = 25,
) -> Any:
    """
    Get all users.
    """
    return admin_service.user_service.get_public_users(
        offset=offset,
        limit=limit,
    )


@router.get(
    "/by-username/{username}",
    response_model=UserPublicAdmin,
)
def get_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
) -> Any:
    """
    Get user by username.
    """
    return admin_service.user_service.get_by_username(
        username=username,
    )


@router.get(
    "/by-id/{id}",
    response_model=UserPublicAdmin,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    id: uuid.UUID,
) -> Any:
    """
    Get user by id.
    """
    return admin_service.user_service.get_by_id(
        id=id,
    )


@router.post(
    "/",
    response_model=UserPublicAdmin,
)
def add(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    user_in: UserRegister,
) -> Any:
    """
    Add a user.
    """
    return admin_service.user_service.add(
        user_in=user_in,
    )


@router.put(
    "/{id}",
    response_model=UserPublicAdmin,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update user.
    """
    return admin_service.user_service.update(
        user_id=id,
        user_in=user_in,
    )


@router.delete(
    "/{id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    id: uuid.UUID,
) -> Any:
    """
    Delete user.
    """
    admin_service.user_service.delete(
        user_id=id,
    )

    return Message(
        message="User deleted",
    )
