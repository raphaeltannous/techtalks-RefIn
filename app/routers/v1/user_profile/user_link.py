import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_profile import UserProfile
from models.user_link import (
    UserLinkIn,
    UserLinkPublic,
    UserLinksPublic,
    UserLinkUpdate,
)
from routers.dependencies import get_current_user_profile, get_user_profile_service
from services.user_profile import UserProfileService

router = APIRouter(
    tags=["user-link"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserLinksPublic,
)
def get_all_by_username(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    """
    Get all user links by username.
    """
    return user_profile_service.link_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{link_id}",
    response_model=UserLinkPublic,
)
def get_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    link_id: uuid.UUID,
) -> Any:
    """
    Get user link by id.
    """
    return user_profile_service.link_service.get_by_id(
        link_id=link_id,
    )


@router.post(
    "/",
    response_model=UserLinkPublic,
)
def add(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    link_in: UserLinkIn,
) -> Any:
    """
    Add new user link.
    """
    return user_profile_service.link_service.add(
        user_profile=user_profile,
        link_in=link_in,
    )


@router.put(
    "/{link_id}",
    response_model=UserLinkPublic,
)
def update(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    link_id: uuid.UUID,
    link_in: UserLinkUpdate,
) -> Any:
    """
    Update user link.
    """
    return user_profile_service.link_service.update(
        user_profile=user_profile,
        link_id=link_id,
        link_in=link_in,
    )


@router.delete(
    "/{link_id}",
    response_model=Message,
)
def delete(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    link_id: uuid.UUID,
) -> Any:
    """
    Delete user link.
    """
    user_profile_service.link_service.delete(
        user_profile=user_profile,
        link_id=link_id,
    )

    return Message(
        message="User link deleted.",
    )
