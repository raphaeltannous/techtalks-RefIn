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
def get_user_projects(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    return user_profile_service.get_all_projects_by_username(
        username=username,
    )


@router.post(
    "/",
    response_model=UserProjectPublic,
)
def add_project(
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
    return user_profile_service.add_project(
        user_profile=user_profile,
        project_in=project_in,
    )


@router.get(
    "/{project_id}",
    response_model=UserProjectPublic,
)
def get_project_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    project_id: uuid.UUID,
) -> Any:
    return user_profile_service.get_project_by_id(
        project_id=project_id,
    )


@router.put(
    "/{project_id}",
    response_model=UserProjectPublic,
)
def update_project(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    project_id: uuid.UUID,
    project_in: UserProjectUpdate,
) -> Any:
    return user_profile_service.update_project(
        user_profile=user_profile,
        project_id=project_id,
        project_in=project_in,
    )


@router.delete(
    "/{project_id}",
    response_model=Message,
)
def delete_project(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    project_id: uuid.UUID,
) -> Any:
    user_profile_service.delete_project(
        user_profile=user_profile,
        project_id=project_id,
    )
    return Message(
        message="User project deleted.",
    )
