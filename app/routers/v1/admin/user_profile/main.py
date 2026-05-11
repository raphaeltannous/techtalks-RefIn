from fastapi import APIRouter

from .certificate import router as user_certificate_router
from .education import router as user_education_router
from .experience import router as user_experience_router
from .language import router as user_language_router
from .link import router as user_link_router
from .profile import router as user_profile_router
from .project import router as user_project_router
from .skill import router as user_skill_router

router = APIRouter()

router.include_router(
    user_profile_router,
    prefix="/profile",
)
router.include_router(
    user_skill_router,
    prefix="/skill",
)
router.include_router(
    user_language_router,
    prefix="/language",
)
router.include_router(
    user_link_router,
    prefix="/link",
)
router.include_router(
    user_project_router,
    prefix="/project",
)
router.include_router(
    user_certificate_router,
    prefix="/certificate",
)
router.include_router(
    user_experience_router,
    prefix="/experience",
)
router.include_router(
    user_education_router,
    prefix="/education",
)
