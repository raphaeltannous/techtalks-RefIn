import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.job import (
    JobIn,
    JobPublic,
    JobsPublic,
    JobUpdate,
)
from models.message import Message
from routers.dependencies import get_admin_service
from services.admin import AdminService

router = APIRouter(
    tags=["admin-job"],
)


@router.get(
    "/all",
    response_model=JobsPublic,
)
def get_all(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    offset: int = 0,
    limit: int = 25,
) -> Any:
    """
    Get all jobs.
    """
    return admin_service.job_service.get_all(
        offset=offset,
        limit=limit,
    )


@router.post(
    "/by-user-id/{user_id}",
    response_model=JobPublic,
)
def add(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    user_id: uuid.UUID,
    job_in: JobIn,
) -> Any:
    """
    Add a new job.
    """
    return admin_service.job_service.add(
        user_id=user_id,
        job_in=job_in,
    )


@router.put(
    "/{job_id}",
    response_model=JobPublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    job_id: uuid.UUID,
    job_in: JobUpdate,
) -> Any:
    """
    Update job.
    """
    return admin_service.job_service.update(
        job_id=job_id,
        job_in=job_in,
    )


@router.delete(
    "/{job_id}",
    response_model=Message,
)
def delete(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    job_id: uuid.UUID,
) -> Any:
    """
    Delete job.
    """
    admin_service.job_service.delete(
        job_id=job_id,
    )

    return Message(
        message="Job is deleted.",
    )


@router.get(
    "/{job_id}",
    response_model=JobPublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    job_id: uuid.UUID,
) -> Any:
    """
    Get job by id.
    """
    return admin_service.job_service.get_by_id(
        job_id=job_id,
    )


@router.get(
    "/by-username/{username}",
    response_model=JobsPublic,
)
def get_all_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
    offset: int = 0,
    limit: int = 25,
) -> Any:
    """
    Get user jobs by username.
    """
    return admin_service.job_service.get_all_by_username(
        username=username,
        offset=offset,
        limit=limit,
    )
