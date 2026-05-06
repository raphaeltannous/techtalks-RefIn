import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_profile import UserProfile
from models.user_project import (
    UserProjectIn,
    UserProjectPublic,
    UserProjectsPublic,
    UserProjectUpdate,
)
from routers.dependencies import get_current_user_profile, get_user_profile_service
from services.user_profile import UserProfileService

router = APIRouter(
    tags=["user-project"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserProjectsPublic,
)
def get_all_by_username(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    """
    Get all user projects by username.
    """
    return user_profile_service.project_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{project_id}",
    response_model=UserProjectPublic,
)
def get_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    project_id: uuid.UUID,
) -> Any:
    """
    Get user project by id.
    """
    return user_profile_service.project_service.get_by_id(
        project_id=project_id,
    )


@router.post(
    "/",
    response_model=UserProjectPublic,
)
def add(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    project_in: UserProjectIn,
) -> Any:
    """
    Add new user project.
    """
    return user_profile_service.project_service.add(
        user_profile=user_profile,
        project_in=project_in,
    )


@router.put(
    "/{project_id}",
    response_model=UserProjectPublic,
)
def update(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    project_id: uuid.UUID,
    project_in: UserProjectUpdate,
) -> Any:
    """
    Update user project.
    """
    return user_profile_service.project_service.update(
        user_profile=user_profile,
        project_id=project_id,
        project_in=project_in,
    )


@router.delete(
    "/{project_id}",
    response_model=Message,
)
def delete(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    project_id: uuid.UUID,
) -> Any:
    """
    Delete user project.
    """
    user_profile_service.project_service.delete(
        user_profile=user_profile,
        project_id=project_id,
    )

    return Message(
        message="User project deleted.",
    )
