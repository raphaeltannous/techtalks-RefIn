import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_project import (
    UserProjectIn,
    UserProjectPublic,
    UserProjectsPublic,
    UserProjectUpdate,
)
from routers.dependencies import (
    get_admin_service,
)
from services.admin import AdminService

router = APIRouter(
    tags=["admin-user-project"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserProjectsPublic,
)
def get_all_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
) -> Any:
    """
    Get all user projects by username.
    """
    return admin_service.user_profile_service.project_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{project_id}",
    response_model=UserProjectPublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    project_id: uuid.UUID,
) -> Any:
    """
    Get user project by id.
    """
    return admin_service.user_profile_service.project_service.get_by_id(
        project_id=project_id,
    )


@router.post(
    "/",
    response_model=UserProjectPublic,
)
def add(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    project_in: UserProjectIn,
) -> Any:
    """
    Add new user project.
    """
    return admin_service.user_profile_service.project_service.add(
        profile_id=profile_id,
        project_in=project_in,
    )


@router.put(
    "/{project_id}",
    response_model=UserProjectPublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    project_id: uuid.UUID,
    project_in: UserProjectUpdate,
) -> Any:
    """
    Update user project.
    """
    return admin_service.user_profile_service.project_service.update(
        project_id=project_id,
        project_in=project_in,
    )


@router.delete(
    "/{project_id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    project_id: uuid.UUID,
) -> Any:
    """
    Delete user project.
    """
    admin_service.user_profile_service.project_service.delete(
        project_id=project_id,
    )

    return Message(
        message="User project deleted.",
    )
