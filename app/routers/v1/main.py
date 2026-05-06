from config import settings
from fastapi import APIRouter

from . import private
from .job.main import main_job_router
from .user_profile.main import main_user_profile_router

api_v1_router = APIRouter()

api_v1_router.include_router(main_user_profile_router, prefix="/user")
api_v1_router.include_router(main_job_router, prefix="/job")

if settings.ENVIRONMENT == "local":
    api_v1_router.include_router(private.router)
