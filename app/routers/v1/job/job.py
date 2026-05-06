import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.job import (
    JobIn,
    JobPublic,
    JobsPublic,
    JobUpdate,
)
from models.user import User
from routers.dependencies import get_current_user, get_job_service
from services.job import JobService

router = APIRouter(
    tags=["job"],
)


@router.get(
    "/all",
    response_model=JobsPublic,
)
def get_all(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    offset: int = 0,
    limit: int = 25,
) -> Any:
    """
    Get all jobs.
    """
    return job_service.get_all(
        offset=offset,
        limit=limit,
    )


@router.post(
    "/",
    response_model=JobPublic,
)
def add(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    job_in: JobIn,
) -> Any:
    """
    Add a new job.
    """
    return job_service.add(
        user=user,
        job_in=job_in,
    )


@router.put(
    "/{job_id}",
    response_model=JobPublic,
)
def update(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    job_id: uuid.UUID,
    job_in: JobUpdate,
) -> Any:
    """
    Update job.
    """
    return job_service.update(
        user=user,
        job_id=job_id,
        job_in=job_in,
    )


@router.delete(
    "/{job_id}",
    response_model=JobPublic,
)
def delete(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    job_id: uuid.UUID,
) -> Any:
    """
    Delete job.
    """
    return job_service.delete(
        user=user,
        job_id=job_id,
    )


@router.get(
    "/{job_id}",
    response_model=JobPublic,
)
def get_by_id(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    job_id: uuid.UUID,
) -> Any:
    """
    Get job by id.
    """
    return job_service.get_by_id(
        job_id=job_id,
    )


@router.get(
    "/by-username/{username}",
    response_model=JobsPublic,
)
def get_all_by_username(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    username: str,
    offset: int = 0,
    limit: int = 25,
) -> Any:
    """
    Get user jobs by username.
    """
    return job_service.get_all_by_username(
        username=username,
        offset=offset,
        limit=limit,
    )
