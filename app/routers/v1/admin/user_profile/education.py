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
from routers.dependencies import (
    get_admin_service,
)
from services.admin import AdminService

router = APIRouter(
    tags=["admin-user-education"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserEducationsPublic,
)
def get_all_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
) -> Any:
    """
    Get all user educations by username.
    """
    return admin_service.user_profile_service.education_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{education_id}",
    response_model=UserEducationPublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    education_id: uuid.UUID,
) -> Any:
    """
    Get user education by id.
    """
    return admin_service.user_profile_service.education_service.get_by_id(
        education_id=education_id,
    )


@router.post(
    "/",
    response_model=UserEducationPublic,
)
def add(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    education_in: UserEducationIn,
) -> Any:
    """
    Add new user education.
    """
    return admin_service.user_profile_service.education_service.add(
        profile_id=profile_id,
        education_in=education_in,
    )


@router.put(
    "/{education_id}",
    response_model=UserEducationPublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    education_id: uuid.UUID,
    education_in: UserEducationUpdate,
) -> Any:
    """
    Update user education.
    """
    return admin_service.user_profile_service.education_service.update(
        education_id=education_id,
        education_in=education_in,
    )


@router.delete(
    "/{education_id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    education_id: uuid.UUID,
) -> Any:
    """
    Delete user education.
    """
    admin_service.user_profile_service.education_service.delete(
        education_id=education_id,
    )

    return Message(
        message="User education deleted.",
    )
