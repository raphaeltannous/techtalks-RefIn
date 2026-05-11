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
from routers.dependencies import (
    get_admin_service,
)
from services.admin import AdminService

router = APIRouter(
    tags=["admin-user-certificate"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserCertificatesPublic,
)
def get_all_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
) -> Any:
    """
    Get all user certificates by username.
    """
    return admin_service.user_profile_service.certificate_service.get_all_by_username(
        username=username,
    )


@router.get(
    "/{certificate_id}",
    response_model=UserCertificatePublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    certificate_id: uuid.UUID,
) -> Any:
    """
    Get user certificate by id.
    """
    return admin_service.user_profile_service.certificate_service.get_by_id(
        certificate_id=certificate_id,
    )


@router.post(
    "/",
    response_model=UserCertificatePublic,
)
def add(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    certificate_in: UserCertificateIn,
) -> Any:
    """
    Add new user certificate.
    """
    return admin_service.user_profile_service.certificate_service.add(
        profile_id=profile_id,
        certificate_in=certificate_in,
    )


@router.put(
    "/{certificate_id}",
    response_model=UserCertificatePublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    certificate_id: uuid.UUID,
    certificate_in: UserCertificateUpdate,
) -> Any:
    """
    Update user certificate.
    """
    return admin_service.user_profile_service.certificate_service.update(
        certificate_id=certificate_id,
        certificate_in=certificate_in,
    )


@router.delete(
    "/{certificate_id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    certificate_id: uuid.UUID,
) -> Any:
    """
    Delete user certificate.
    """
    admin_service.user_profile_service.certificate_service.delete(
        certificate_id=certificate_id,
    )

    return Message(
        message="User certificate deleted.",
    )
