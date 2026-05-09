import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.job_application import (
    JobApplicationPublic,
    JobApplicationsPublic,
    JobApplicationUpdate,
)
from models.message import Message
from models.user import User
from routers.dependencies import get_current_user, get_job_service
from services.job import JobService

router = APIRouter(
    tags=["job-application"],
)


@router.get(
    "/by-job/{job_id}",
    response_model=JobApplicationsPublic,
)
def get_all_by_job_id(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    job_id: uuid.UUID,
) -> Any:
    """
    Get all applications for a job.
    """
    return job_service.application_service.get_all_by_job_id(
        user=user,
        job_id=job_id,
    )


@router.post(
    "/by-job/{job_id}",
    response_model=JobApplicationPublic,
)
def apply(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    job_id: uuid.UUID,
) -> Any:
    """
    Apply to a job.
    """
    return job_service.application_service.apply(
        user=user,
        job_id=job_id,
    )


@router.get(
    "/my-applications",
    response_model=JobApplicationsPublic,
)
def get_all_by_user(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
) -> Any:
    """
    Get all applications for current logged in user.
    """
    return job_service.application_service.get_all_by_user(
        user=user,
    )


@router.get(
    "/{application_id}",
    response_model=JobApplicationPublic,
)
def get_by_id(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    application_id: uuid.UUID,
) -> Any:
    """
    Get job application by id.
    """
    return job_service.application_service.get_by_id(
        user=user,
        application_id=application_id,
    )


@router.put(
    "/{application_id}",
    response_model=JobApplicationPublic,
)
def update(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    application_id: uuid.UUID,
    application_in: JobApplicationUpdate,
) -> Any:
    """
    Update a job application requirement.
    """
    return job_service.application_service.update(
        user=user,
        application_id=application_id,
        application_in=application_in,
    )


@router.delete(
    "/{application_id}",
    response_model=Message,
)
def delete(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    application_id: uuid.UUID,
) -> Any:
    """
    Delete a job application requirement.
    """
    job_service.application_service.delete(
        user=user,
        application_id=application_id,
    )

    return Message(
        message="Job application deleted.",
    )
