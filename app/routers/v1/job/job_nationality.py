import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.job_nationality import (
    JobNationalitiesPublic,
    JobNationalityIn,
    JobNationalityPublic,
    JobNationalityUpdate,
)
from models.message import Message
from models.user import User
from routers.dependencies import get_current_user, get_job_service
from services.job import JobService

router = APIRouter(
    tags=["job-nationality"],
)


@router.get(
    "/by-job/{job_id}",
    response_model=JobNationalitiesPublic,
)
def get_all_nationalities_by_job_id(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    job_id: uuid.UUID,
) -> Any:
    """
    Get all nationalities for a job.
    """
    return job_service.nationality_service.get_all_by_job_id(
        job_id=job_id,
    )


@router.post(
    "/by-job/{job_id}",
    response_model=JobNationalityPublic,
)
def add_nationality(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    job_id: uuid.UUID,
    nationality_in: JobNationalityIn,
) -> Any:
    """
    Add a nationality requirement to a job.
    """
    return job_service.nationality_service.add(
        user=user,
        job_id=job_id,
        nationality_in=nationality_in,
    )


@router.get(
    "/{nationality_id}",
    response_model=JobNationalityPublic,
)
def get_nationality_by_id(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    nationality_id: uuid.UUID,
) -> Any:
    """
    Get job nationality by id.
    """
    return job_service.nationality_service.get_by_id(
        nationality_id=nationality_id,
    )


@router.put(
    "/{nationality_id}",
    response_model=JobNationalityPublic,
)
def update_nationality(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    nationality_id: uuid.UUID,
    nationality_in: JobNationalityUpdate,
) -> Any:
    """
    Update a job nationality requirement.
    """
    return job_service.nationality_service.update(
        user=user,
        nationality_id=nationality_id,
        nationality_in=nationality_in,
    )


@router.delete(
    "/{nationality_id}",
    response_model=Message,
)
def delete_nationality(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    nationality_id: uuid.UUID,
) -> Any:
    """
    Delete a job nationality requirement.
    """
    job_service.nationality_service.delete(
        user=user,
        nationality_id=nationality_id,
    )
    return Message(
        message="Job nationality deleted.",
    )
