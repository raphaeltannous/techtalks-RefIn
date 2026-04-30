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
def get_user_educations(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    return user_profile_service.get_all_educations_by_username(
        username=username,
    )


@router.post(
    "/",
    response_model=UserEducationPublic,
)
def add_education(
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
    return user_profile_service.add_education(
        user_profile=user_profile,
        education_in=education_in,
    )


@router.get(
    "/{education_id}",
    response_model=UserEducationPublic,
)
def get_education_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    education_id: uuid.UUID,
) -> Any:
    return user_profile_service.get_education_by_id(
        education_id=education_id,
    )


@router.put(
    "/{education_id}",
    response_model=UserEducationPublic,
)
def update_education(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    education_id: uuid.UUID,
    education_in: UserEducationUpdate,
) -> Any:
    return user_profile_service.update_education(
        user_profile=user_profile,
        education_id=education_id,
        education_in=education_in,
    )


@router.delete(
    "/{education_id}",
    response_model=Message,
)
def delete_education(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    education_id: uuid.UUID,
) -> Any:
    user_profile_service.delete_education(
        user_profile=user_profile,
        education_id=education_id,
    )
    return Message(
        message="User education deleted.",
    )
