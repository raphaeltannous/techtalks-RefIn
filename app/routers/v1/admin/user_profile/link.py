import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_link import (
    UserLinkIn,
    UserLinkPublic,
    UserLinksPublic,
    UserLinkUpdate,
)
from routers.dependencies import (
    get_admin_service,
)
from services.admin import AdminService

router = APIRouter(
    tags=["admin-user-link"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserLinksPublic,
)
def get_all_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
) -> Any:
    """
    Get all user links by username.
    """
    return admin_service.user_profile_service.link_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{link_id}",
    response_model=UserLinkPublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    link_id: uuid.UUID,
) -> Any:
    """
    Get user link by id.
    """
    return admin_service.user_profile_service.link_service.get_by_id(
        link_id=link_id,
    )


@router.post(
    "/",
    response_model=UserLinkPublic,
)
def add(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    link_in: UserLinkIn,
) -> Any:
    """
    Add new user link.
    """
    return admin_service.user_profile_service.link_service.add(
        profile_id=profile_id,
        link_in=link_in,
    )


@router.put(
    "/{link_id}",
    response_model=UserLinkPublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    link_id: uuid.UUID,
    link_in: UserLinkUpdate,
) -> Any:
    """
    Update user link.
    """
    return admin_service.user_profile_service.link_service.update(
        link_id=link_id,
        link_in=link_in,
    )


@router.delete(
    "/{link_id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    link_id: uuid.UUID,
) -> Any:
    """
    Delete user link.
    """
    admin_service.user_profile_service.link_service.delete(
        link_id=link_id,
    )

    return Message(
        message="User link deleted.",
    )
