import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_skill import (
    UserSkillIn,
    UserSkillPublic,
    UserSkillsPublic,
    UserSkillUpdate,
)
from routers.dependencies import (
    get_admin_service,
)
from services.admin import AdminService

router = APIRouter(
    tags=["admin-user-skill"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserSkillsPublic,
)
def get_all_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
) -> Any:
    """
    Get all user skills by username.
    """
    return admin_service.user_profile_service.skill_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{skill_id}",
    response_model=UserSkillPublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    skill_id: uuid.UUID,
) -> Any:
    """
    Get user skill by id.
    """
    return admin_service.user_profile_service.skill_service.get_by_id(
        skill_id=skill_id,
    )


@router.post(
    "/",
    response_model=UserSkillPublic,
)
def add(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    skill_in: UserSkillIn,
) -> Any:
    """
    Add new user skill.
    """
    return admin_service.user_profile_service.skill_service.add(
        profile_id=profile_id,
        skill_in=skill_in,
    )


@router.put(
    "/{skill_id}",
    response_model=UserSkillPublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    skill_id: uuid.UUID,
    skill_in: UserSkillUpdate,
) -> Any:
    """
    Update user skill.
    """
    return admin_service.user_profile_service.skill_service.update(
        skill_id=skill_id,
        skill_in=skill_in,
    )


@router.delete(
    "/{skill_id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    skill_id: uuid.UUID,
) -> Any:
    """
    Delete user skill.
    """
    admin_service.user_profile_service.skill_service.delete(
        skill_id=skill_id,
    )

    return Message(
        message="User skill deleted.",
    )
