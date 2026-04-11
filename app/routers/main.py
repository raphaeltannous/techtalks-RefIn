from fastapi import APIRouter

from . import login, users

api_router = APIRouter()


api_router.include_router(login.router)
