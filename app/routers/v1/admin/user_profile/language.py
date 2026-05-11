import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_language import (
    UserLanguageIn,
    UserLanguagePublic,
    UserLanguagesPublic,
    UserLanguageUpdate,
)
from routers.dependencies import (
    get_admin_service,
)
from services.admin import AdminService

router = APIRouter(
    tags=["admin-user-language"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserLanguagesPublic,
)
def get_all_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
) -> Any:
    """
    Get all user languages by username.
    """
    return admin_service.user_profile_service.language_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{language_id}",
    response_model=UserLanguagePublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    language_id: uuid.UUID,
) -> Any:
    """
    Get user language by id.
    """
    return admin_service.user_profile_service.language_service.get_by_id(
        language_id=language_id,
    )


@router.post(
    "/",
    response_model=UserLanguagePublic,
)
def add(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    language_in: UserLanguageIn,
) -> Any:
    """
    Add new user language.
    """
    return admin_service.user_profile_service.language_service.add(
        profile_id=profile_id,
        language_in=language_in,
    )


@router.put(
    "/{language_id}",
    response_model=UserLanguagePublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    language_id: uuid.UUID,
    language_in: UserLanguageUpdate,
) -> Any:
    """
    Update user language.
    """
    return admin_service.user_profile_service.language_service.update(
        language_id=language_id,
        language_in=language_in,
    )


@router.delete(
    "/{language_id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    language_id: uuid.UUID,
) -> Any:
    """
    Delete user language.
    """
    admin_service.user_profile_service.language_service.delete(
        language_id=language_id,
    )

    return Message(
        message="User language deleted.",
    )
