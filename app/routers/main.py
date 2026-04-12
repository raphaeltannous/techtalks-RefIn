from config import settings
from fastapi import APIRouter

from .v1.main import api_v1_router

api_router = APIRouter()

api_router.include_router(api_v1_router, prefix=settings.API_VERSION_STRING)
