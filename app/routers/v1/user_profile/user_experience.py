import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_profile import UserProfile
from models.user_experience import (
    UserExperienceIn,
    UserExperiencePublic,
    UserExperiencesPublic,
    UserExperienceUpdate,
)
from routers.dependencies import get_current_user_profile, get_user_profile_service
from services.user_profile import UserProfileService

router = APIRouter(
    tags=["user-experience"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserExperiencesPublic,
)
def get_all_by_username(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    """
    Get all user experiences by username.
    """
    return user_profile_service.experience_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{experience_id}",
    response_model=UserExperiencePublic,
)
def get_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    experience_id: uuid.UUID,
) -> Any:
    """
    Get user experience by id.
    """
    return user_profile_service.experience_service.get_by_id(
        experience_id=experience_id,
    )


@router.post(
    "/",
    response_model=UserExperiencePublic,
)
def add(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    experience_in: UserExperienceIn,
) -> Any:
    """
    Add new user experience.
    """
    return user_profile_service.experience_service.add(
        user_profile=user_profile,
        experience_in=experience_in,
    )


@router.put(
    "/{experience_id}",
    response_model=UserExperiencePublic,
)
def update(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    experience_id: uuid.UUID,
    experience_in: UserExperienceUpdate,
) -> Any:
    """
    Update user experience.
    """
    return user_profile_service.experience_service.update(
        user_profile=user_profile,
        experience_id=experience_id,
        experience_in=experience_in,
    )


@router.delete(
    "/{experience_id}",
    response_model=Message,
)
def delete(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    experience_id: uuid.UUID,
) -> Any:
    """
    Delete user experience.
    """
    user_profile_service.experience_service.delete(
        user_profile=user_profile,
        experience_id=experience_id,
    )

    return Message(
        message="User experience deleted.",
    )
