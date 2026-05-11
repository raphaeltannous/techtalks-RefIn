import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.job_application import (
    JobApplicationPublic,
    JobApplicationsPublic,
    JobApplicationUpdate,
)
from models.message import Message
from routers.dependencies import get_admin_service
from services.admin import AdminService

router = APIRouter(
    tags=["admin-job-application"],
)


@router.get(
    "/by-job/{job_id}",
    response_model=JobApplicationsPublic,
)
def get_all_by_job_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    job_id: uuid.UUID,
) -> Any:
    """
    Get all applications for a job.
    """
    return admin_service.job_service.application_service.get_all_by_job_id(
        job_id=job_id,
    )


@router.post(
    "/by-job/{job_id}",
    response_model=JobApplicationPublic,
)
def apply(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    user_id: uuid.UUID,
    job_id: uuid.UUID,
) -> Any:
    """
    Apply to a job.
    """
    return admin_service.job_service.application_service.apply(
        user_id=user_id,
        job_id=job_id,
    )


@router.get(
    "/by-user-id/{user_id}",
    response_model=JobApplicationsPublic,
)
def get_all_by_user(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    user_id: uuid.UUID,
) -> Any:
    """
    Get all applications for user.
    """
    return admin_service.job_service.application_service.get_all_by_user(
        user_id=user_id,
    )


@router.get(
    "/{application_id}",
    response_model=JobApplicationPublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    application_id: uuid.UUID,
) -> Any:
    """
    Get job application by id.
    """
    return admin_service.job_service.application_service.get_by_id(
        application_id=application_id,
    )


@router.put(
    "/{application_id}",
    response_model=JobApplicationPublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    application_id: uuid.UUID,
    application_in: JobApplicationUpdate,
) -> Any:
    """
    Update a job application.
    """
    return admin_service.job_service.application_service.update(
        application_id=application_id,
        application_in=application_in,
    )


@router.delete(
    "/{application_id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    application_id: uuid.UUID,
) -> Any:
    """
    Delete a job application.
    """
    admin_service.job_service.application_service.delete(
        application_id=application_id,
    )

    return Message(
        message="Job application deleted.",
    )
