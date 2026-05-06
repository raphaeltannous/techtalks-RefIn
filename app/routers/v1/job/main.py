from fastapi import APIRouter

from .job import router as job_router

main_job_router = APIRouter(
    tags=["job"],
)

main_job_router.include_router(
    job_router,
    prefix="",
)
