import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.user_certificate import (
    UserCertificateIn,
    UserCertificatePublic,
    UserCertificatesPublic,
    UserCertificateUpdate,
)
from models.user_profile import UserProfile
from routers.dependencies import get_current_user_profile, get_user_profile_service
from services.user_profile import UserProfileService

router = APIRouter(
    tags=["user-certificate"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserCertificatesPublic,
)
def get_user_certificates(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    return user_profile_service.get_all_certificates_by_username(
        username=username,
    )


@router.post(
    "/",
    response_model=UserCertificatePublic,
)
def add_certificate(
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
    return user_profile_service.add_certificate(
        user_profile=user_profile,
        certificate_in=certificate_in,
    )


@router.get(
    "/{certificate_id}",
    response_model=UserCertificatePublic,
)
def get_certificate_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    certificate_id: uuid.UUID,
) -> Any:
    return user_profile_service.get_certificate_by_id(
        certificate_id=certificate_id,
    )


@router.put(
    "/{certificate_id}",
    response_model=UserCertificatePublic,
)
def update_certificate(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    certificate_id: uuid.UUID,
    certificate_in: UserCertificateUpdate,
) -> Any:
    return user_profile_service.update_certificate(
        user_profile=user_profile,
        certificate_id=certificate_id,
        certificate_in=certificate_in,
    )


@router.delete(
    "/{certificate_id}",
    response_model=Message,
)
def delete_certificate(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    certificate_id: uuid.UUID,
) -> Any:
    user_profile_service.delete_certificate(
        user_profile=user_profile,
        certificate_id=certificate_id,
    )
    return Message(
        message="User certificate deleted.",
    )
