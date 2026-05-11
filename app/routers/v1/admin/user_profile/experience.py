import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_experience import (
    UserExperienceIn,
    UserExperiencePublic,
    UserExperiencesPublic,
    UserExperienceUpdate,
)
from routers.dependencies import (
    get_admin_service,
)
from services.admin import AdminService

router = APIRouter(
    tags=["admin-user-experience"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserExperiencesPublic,
)
def get_all_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
) -> Any:
    """
    Get all user experiences by username.
    """
    return admin_service.user_profile_service.experience_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{experience_id}",
    response_model=UserExperiencePublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    experience_id: uuid.UUID,
) -> Any:
    """
    Get user experience by id.
    """
    return admin_service.user_profile_service.experience_service.get_by_id(
        experience_id=experience_id,
    )


@router.post(
    "/",
    response_model=UserExperiencePublic,
)
def add(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    experience_in: UserExperienceIn,
) -> Any:
    """
    Add new user experience.
    """
    return admin_service.user_profile_service.experience_service.add(
        profile_id=profile_id,
        experience_in=experience_in,
    )


@router.put(
    "/{experience_id}",
    response_model=UserExperiencePublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    experience_id: uuid.UUID,
    experience_in: UserExperienceUpdate,
) -> Any:
    """
    Update user experience.
    """
    return admin_service.user_profile_service.experience_service.update(
        experience_id=experience_id,
        experience_in=experience_in,
    )


@router.delete(
    "/{experience_id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    experience_id: uuid.UUID,
) -> Any:
    """
    Delete user experience.
    """
    admin_service.user_profile_service.experience_service.delete(
        experience_id=experience_id,
    )

    return Message(
        message="User experience deleted.",
    )
