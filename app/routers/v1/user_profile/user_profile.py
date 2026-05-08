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
from models.user_profile import UserProfile, UserProfilePublic, UserProfileUpdate
from routers.dependencies import get_current_user_profile, get_user_profile_service
from services.user_profile import UserProfileService

router = APIRouter(
    tags=["user-profile"],
)


@router.get(
    "/by-username/{username}",
    response_model=UserProfilePublic,
)
def get_by_username(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    return user_profile_service.get_by_username(
        username=username,
    )


@router.get(
    "/by-id/{user_id}",
    response_model=UserProfilePublic,
)
def get_by_id(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_id: uuid.UUID,
) -> Any:
    return user_profile_service.get_by_user_id(
        user_id=user_id,
    )


@router.put(
    "/",
    response_model=UserProfilePublic,
)
def update(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    profile_in: UserProfileUpdate,
) -> Any:
    return user_profile_service.update(
        user_profile=user_profile,
        profile_in=profile_in,
    )


@router.put(
    "/profile-picture",
    response_model=UserProfilePublic,
)
async def upload_profile_picture(
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    file: UploadFile = File(...),
) -> Any:
    contents = await file.read()

    if len(contents) > settings.MAX_USER_PROFILE_UPLOAD_SIZE_BYTES:
        raise UserProfileUploadSizeExceededError()

    return user_profile_service.update_profile_picture(
        user_profile=user_profile,
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
    "/banner",
    response_model=UserProfilePublic,
)
async def upload_profile_banner(
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    file: UploadFile = File(...),
) -> Any:
    contents = await file.read()

    if len(contents) > settings.MAX_USER_PROFILE_UPLOAD_SIZE_BYTES:
        raise UserProfileUploadSizeExceededError()

    return user_profile_service.update_banner(
        user_profile=user_profile,
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
