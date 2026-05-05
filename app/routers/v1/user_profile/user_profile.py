from typing import Annotated, Any

from config import settings
from exceptions import UserProfileUploadSizeExceededError
from fastapi import APIRouter, Depends, File, UploadFile
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
def get_user_profile(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    username: str,
) -> Any:
    return user_profile_service.get_by_username(
        username=username,
    )


@router.put(
    "/",
    response_model=UserProfilePublic,
)
def update_profile(
    *,
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    profile_in: UserProfileUpdate,
) -> Any:
    return user_profile_service.update_profile(
        user_profile=user_profile,
        profile_in=profile_in,
    )


@router.patch(
    "/profile-picture",
    response_model=UserProfilePublic,
)
async def upload_profile_picture(
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    user_profile: Annotated[UserProfile, Depends(get_current_user_profile)],
    file: UploadFile = File(...),
):
    contents = await file.read()

    if len(contents) > settings.MAX_USER_PROFILE_UPLOAD_SIZE_BYTES:
        raise UserProfileUploadSizeExceededError()

    return user_profile_service.update_profile_picture(
        user_profile=user_profile,
        image_bytes=contents,
    )
