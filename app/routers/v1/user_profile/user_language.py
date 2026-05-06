import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_profile import UserProfile
from models.user_language import (
    UserLanguageIn,
    UserLanguagePublic,
    UserLanguagesPublic,
    UserLanguageUpdate,
)
from routers.dependencies import get_current_user_profile, get_user_profile_service
from services.user_profile import UserProfileService

router = APIRouter(
    tags=["user-language"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserLanguagesPublic,
)
def get_all_by_username(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    """
    Get all user languages by username.
    """
    return user_profile_service.language_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{language_id}",
    response_model=UserLanguagePublic,
)
def get_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    language_id: uuid.UUID,
) -> Any:
    """
    Get user language by id.
    """
    return user_profile_service.language_service.get_by_id(
        language_id=language_id,
    )


@router.post(
    "/",
    response_model=UserLanguagePublic,
)
def add(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    language_in: UserLanguageIn,
) -> Any:
    """
    Add new user language.
    """
    return user_profile_service.language_service.add(
        user_profile=user_profile,
        language_in=language_in,
    )


@router.put(
    "/{language_id}",
    response_model=UserLanguagePublic,
)
def update(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    language_id: uuid.UUID,
    language_in: UserLanguageUpdate,
) -> Any:
    """
    Update user language.
    """
    return user_profile_service.language_service.update(
        user_profile=user_profile,
        language_id=language_id,
        language_in=language_in,
    )


@router.delete(
    "/{language_id}",
    response_model=Message,
)
def delete(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    language_id: uuid.UUID,
) -> Any:
    """
    Delete user language.
    """
    user_profile_service.language_service.delete(
        user_profile=user_profile,
        language_id=language_id,
    )

    return Message(
        message="User language deleted.",
    )
