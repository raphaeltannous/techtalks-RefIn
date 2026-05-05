import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_profile import UserProfile
from models.user_certificate import (
    UserCertificateIn,
    UserCertificatePublic,
    UserCertificatesPublic,
    UserCertificateUpdate,
)
from routers.dependencies import get_current_user_profile, get_user_profile_service
from services.user_profile import UserProfileService

router = APIRouter(
    tags=["user-certificate"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserCertificatesPublic,
)
def get_all_by_username(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    """
    Get all user certificates by username.
    """
    return user_profile_service.certificate_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{certificate_id}",
    response_model=UserCertificatePublic,
)
def get_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    certificate_id: uuid.UUID,
) -> Any:
    """
    Get user certificate by id.
    """
    return user_profile_service.certificate_service.get_by_id(
        certificate_id=certificate_id,
    )


@router.post(
    "/",
    response_model=UserCertificatePublic,
)
def add(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    certificate_in: UserCertificateIn,
) -> Any:
    """
    Add new user certificate.
    """
    return user_profile_service.certificate_service.add(
        user_profile=user_profile,
        certificate_in=certificate_in,
    )


@router.put(
    "/{certificate_id}",
    response_model=UserCertificatePublic,
)
def update(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    certificate_id: uuid.UUID,
    certificate_in: UserCertificateUpdate,
) -> Any:
    """
    Update user certificate.
    """
    return user_profile_service.certificate_service.update(
        user_profile=user_profile,
        certificate_id=certificate_id,
        certificate_in=certificate_in,
    )


@router.delete(
    "/{certificate_id}",
    response_model=Message,
)
def delete(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    certificate_id: uuid.UUID,
) -> Any:
    """
    Delete user certificate.
    """
    user_profile_service.certificate_service.delete(
        user_profile=user_profile,
        certificate_id=certificate_id,
    )

    return Message(
        message="User certificate deleted.",
    )
