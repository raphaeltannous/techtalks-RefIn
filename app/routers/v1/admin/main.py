from fastapi import APIRouter

from .job.main import router as admin_job_router
from .user_profile.main import router as user_profile_router

router = APIRouter()

router.include_router(
    admin_job_router,
    prefix="/job",
)
router.include_router(
    user_profile_router,
    prefix="/user",
)
