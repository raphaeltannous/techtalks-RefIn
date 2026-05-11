from fastapi import APIRouter

from .application import router as job_application_router
from .job import router as job_router
from .language import router as job_language_router
from .nationality import router as job_nationality_router

router = APIRouter(
    tags=["admin-job"],
)

router.include_router(
    job_router,
    prefix="",
)
router.include_router(
    job_language_router,
    prefix="/language",
)
router.include_router(
    job_application_router,
    prefix="/application",
)
router.include_router(
    job_nationality_router,
    prefix="/nationality",
)
