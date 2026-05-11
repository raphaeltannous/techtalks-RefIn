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
from routers.dependencies import get_admin_service
from services.admin import AdminService

router = APIRouter(
    tags=["job-nationality"],
)


@router.get(
    "/by-job/{job_id}",
    response_model=JobNationalitiesPublic,
)
def get_all_nationalities_by_job_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    job_id: uuid.UUID,
) -> Any:
    """
    Get all nationalities for a job.
    """
    return admin_service.job_service.nationality_service.get_all_by_job_id(
        job_id=job_id,
    )


@router.post(
    "/by-job/{job_id}",
    response_model=JobNationalityPublic,
)
def add_nationality(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    job_id: uuid.UUID,
    nationality_in: JobNationalityIn,
) -> Any:
    """
    Add a nationality requirement to a job.
    """
    return admin_service.job_service.nationality_service.add(
        job_id=job_id,
        nationality_in=nationality_in,
    )


@router.get(
    "/{nationality_id}",
    response_model=JobNationalityPublic,
)
def get_nationality_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    nationality_id: uuid.UUID,
) -> Any:
    """
    Get job nationality by id.
    """
    return admin_service.job_service.nationality_service.get_by_id(
        nationality_id=nationality_id,
    )


@router.put(
    "/{nationality_id}",
    response_model=JobNationalityPublic,
)
def update_nationality(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    nationality_id: uuid.UUID,
    nationality_in: JobNationalityUpdate,
) -> Any:
    """
    Update a job nationality requirement.
    """
    return admin_service.job_service.nationality_service.update(
        nationality_id=nationality_id,
        nationality_in=nationality_in,
    )


@router.delete(
    "/{nationality_id}",
    response_model=Message,
)
def delete_nationality(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    nationality_id: uuid.UUID,
) -> Any:
    """
    Delete a job nationality requirement.
    """
    admin_service.job_service.nationality_service.delete(
        nationality_id=nationality_id,
    )

    return Message(
        message="Job nationality deleted.",
    )
