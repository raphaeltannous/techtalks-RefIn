from fastapi import APIRouter

from .job import router as job_router
from .job_application import router as job_application_router
from .job_language import router as job_language_router

main_job_router = APIRouter(
    tags=["job"],
)

main_job_router.include_router(
    job_router,
    prefix="",
)
main_job_router.include_router(
    job_language_router,
    prefix="/language",
)
main_job_router.include_router(
    job_application_router,
    prefix="/application",
)
