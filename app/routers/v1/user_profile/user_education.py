import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_education import (
    UserEducationIn,
    UserEducationPublic,
    UserEducationsPublic,
    UserEducationUpdate,
)
from models.user_profile import UserProfile
from routers.dependencies import get_current_user_profile, get_user_profile_service
from services.user_profile import UserProfileService

router = APIRouter(
    tags=["user-education"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserEducationsPublic,
)
def get_all_by_username(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    """
    Get all user educations by username.
    """
    return user_profile_service.education_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{education_id}",
    response_model=UserEducationPublic,
)
def get_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    education_id: uuid.UUID,
) -> Any:
    """
    Get user education by id.
    """
    return user_profile_service.education_service.get_by_id(
        education_id=education_id,
    )


@router.post(
    "/",
    response_model=UserEducationPublic,
)
def add(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    education_in: UserEducationIn,
) -> Any:
    """
    Add new user education.
    """
    return user_profile_service.education_service.add(
        user_profile=user_profile,
        education_in=education_in,
    )


@router.put(
    "/{education_id}",
    response_model=UserEducationPublic,
)
def update(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    education_id: uuid.UUID,
    education_in: UserEducationUpdate,
) -> Any:
    """
    Update user education.
    """
    return user_profile_service.education_service.update(
        user_profile=user_profile,
        education_id=education_id,
        education_in=education_in,
    )


@router.delete(
    "/{education_id}",
    response_model=Message,
)
def delete(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    education_id: uuid.UUID,
) -> Any:
    """
    Delete user education.
    """
    user_profile_service.education_service.delete(
        user_profile=user_profile,
        education_id=education_id,
    )

    return Message(
        message="User education deleted.",
    )
