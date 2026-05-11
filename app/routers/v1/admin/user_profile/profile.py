import uuid
from pathlib import PurePath
from typing import Annotated, Any

from config import settings
from exceptions import (
    UserProfileBannerNotFound,
    UserProfilePictureNotFound,
    UserProfileUploadSizeExceededError,
)
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from models.user_profile import UserProfilePublic, UserProfileUpdate
from routers.dependencies import get_admin_service
from services.admin import AdminService

router = APIRouter(
    tags=["admin-user-profile"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserProfilePublic,
)
def get_by_username(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    username: str,
) -> Any:
    return admin_service.user_profile_service.get_by_username(
        username=username,
    )


@router.get(
    "/by-id/{user_id}",
    response_model=UserProfilePublic,
)
def get_by_id(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    user_id: uuid.UUID,
) -> Any:
    return admin_service.user_profile_service.get_by_user_id(
        user_id=user_id,
    )


@router.put(
    "/{profile_id}",
    response_model=UserProfilePublic,
)
def update(
    *,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    profile_in: UserProfileUpdate,
) -> Any:
    return admin_service.user_profile_service.update(
        profile_id=profile_id,
        profile_in=profile_in,
    )


@router.put(
    "/profile-picture/{profile_id}",
    response_model=UserProfilePublic,
)
async def upload_profile_picture(
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    file: UploadFile = File(...),
) -> Any:
    contents = await file.read()

    if len(contents) > settings.MAX_USER_PROFILE_UPLOAD_SIZE_BYTES:
        raise UserProfileUploadSizeExceededError()

    return admin_service.user_profile_service.update_profile_picture(
        profile_id=profile_id,
        image_bytes=contents,
    )


@router.get(
    "/profile-picture/{filename}",
    response_class=FileResponse,
)
async def get_profile_picture(
    filename: str,
) -> Any:
    filename = PurePath(filename).name

    file_path = settings.USER_PROFILE_PICTURES_DIRECTORY.joinpath(filename).absolute()

    if not file_path.exists():
        raise UserProfilePictureNotFound()

    return file_path


@router.put(
    "/banner/{profile_id}",
    response_model=UserProfilePublic,
)
async def upload_profile_banner(
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    profile_id: uuid.UUID,
    file: UploadFile = File(...),
) -> Any:
    contents = await file.read()

    if len(contents) > settings.MAX_USER_PROFILE_UPLOAD_SIZE_BYTES:
        raise UserProfileUploadSizeExceededError()

    return admin_service.user_profile_service.update_banner(
        profile_id=profile_id,
        image_bytes=contents,
    )


@router.get(
    "/banner/{filename}",
    response_class=FileResponse,
)
async def get_profile_banner(
    filename: str,
) -> Any:
    filename = PurePath(filename).name

    file_path = settings.USER_PROFILE_BANNERS_DIRECTORY.joinpath(filename).absolute()

    if not file_path.exists():
        raise UserProfileBannerNotFound()

    return file_path
