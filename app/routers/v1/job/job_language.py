import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.job_language import (
    JobLanguageIn,
    JobLanguagePublic,
    JobLanguagesPublic,
    JobLanguageUpdate,
)
from models.message import Message
from models.user import User
from routers.dependencies import get_current_user, get_job_service
from services.job import JobService

router = APIRouter(
    tags=["job-language"],
)


@router.get(
    "/by-job/{job_id}",
    response_model=JobLanguagesPublic,
)
def get_all_languages_by_job_id(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    job_id: uuid.UUID,
) -> Any:
    """
    Get all languages for a job.
    """
    return job_service.language_service.get_all_by_job_id(
        job_id=job_id,
    )


@router.post(
    "/by-job/{job_id}",
    response_model=JobLanguagePublic,
)
def add_language(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    job_id: uuid.UUID,
    language_in: JobLanguageIn,
) -> Any:
    """
    Add a language requirement to a job.
    """
    return job_service.language_service.add(
        user=user,
        job_id=job_id,
        language_in=language_in,
    )


@router.get(
    "/{language_id}",
    response_model=JobLanguagePublic,
)
def get_language_by_id(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    language_id: uuid.UUID,
) -> Any:
    """
    Get job language by id.
    """
    return job_service.language_service.get_by_id(
        language_id=language_id,
    )


@router.put(
    "/{language_id}",
    response_model=JobLanguagePublic,
)
def update_language(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    language_id: uuid.UUID,
    language_in: JobLanguageUpdate,
) -> Any:
    """
    Update a job language requirement.
    """
    return job_service.language_service.update(
        user=user,
        language_id=language_id,
        language_in=language_in,
    )


@router.delete(
    "/{language_id}",
    response_model=Message,
)
def delete_language(
    *,
    job_service: Annotated[JobService, Depends(get_job_service)],
    user: Annotated[User, Depends(get_current_user)],
    language_id: uuid.UUID,
) -> Any:
    """
    Delete a job language requirement.
    """
    job_service.language_service.delete(
        user=user,
        language_id=language_id,
    )

    return Message(
        message="Job language deleted.",
    )
