from fastapi import APIRouter, Depends
from routers.dependencies import get_current_active_admin

from .admin.main import router as admin_router
from .job.main import main_job_router
from .notification import router as notification_router
from .user_profile.main import main_user_profile_router

api_v1_router = APIRouter()

api_v1_router.include_router(
    admin_router,
    prefix="/admin",
    dependencies=[
        Depends(get_current_active_admin),
    ],
)
api_v1_router.include_router(main_job_router, prefix="/job")
api_v1_router.include_router(main_user_profile_router, prefix="/user")
api_v1_router.include_router(notification_router, prefix="/notification")
