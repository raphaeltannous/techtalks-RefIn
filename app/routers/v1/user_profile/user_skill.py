import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_profile import UserProfile
from models.user_skill import (
    UserSkillIn,
    UserSkillPublic,
    UserSkillsPublic,
    UserSkillUpdate,
)
from routers.dependencies import get_current_user_profile, get_user_profile_service
from services.user_profile import UserProfileService

router = APIRouter(
    tags=["user-skill"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserSkillsPublic,
)
def get_all_by_username(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    """
    Get all user skills by username.
    """
    return user_profile_service.skill_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{skill_id}",
    response_model=UserSkillPublic,
)
def get_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    skill_id: uuid.UUID,
) -> Any:
    """
    Get user skill by id.
    """
    return user_profile_service.skill_service.get_by_id(
        skill_id=skill_id,
    )


@router.post(
    "/",
    response_model=UserSkillPublic,
)
def add(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    skill_in: UserSkillIn,
) -> Any:
    """
    Add new user skill.
    """
    return user_profile_service.skill_service.add(
        user_profile=user_profile,
        skill_in=skill_in,
    )


@router.put(
    "/{skill_id}",
    response_model=UserSkillPublic,
)
def update(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    skill_id: uuid.UUID,
    skill_in: UserSkillUpdate,
) -> Any:
    """
    Update user skill.
    """
    return user_profile_service.skill_service.update(
        user_profile=user_profile,
        skill_id=skill_id,
        skill_in=skill_in,
    )


@router.delete(
    "/{skill_id}",
    response_model=Message,
)
def delete(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    skill_id: uuid.UUID,
) -> Any:
    """
    Delete user skill.
    """
    user_profile_service.skill_service.delete(
        user_profile=user_profile,
        skill_id=skill_id,
    )

    return Message(
        message="User skill deleted.",
    )
