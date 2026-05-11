from typing import Annotated

import jwt
import security.jwt_token
from config import settings
from exceptions import UserProfileNotFoundError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from models.jwt import TokenPayload
from models.user import User
from models.user_profile import UserProfile
from pydantic import ValidationError
from services.job import JobService
from services.notification import NotificationService
from services.user import UserService
from services.user_profile import UserProfileService

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_VERSION_1_STRING}/auth/login"
)


TokenDep = Annotated[str, Depends(reusable_oauth2)]


# Create dependencies for services
def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service


def get_user_profile_service(request: Request) -> UserProfileService:
    return request.app.state.user_profile_service


def get_job_service(request: Request) -> JobService:
    return request.app.state.job_service


def get_notification_service(request: Request) -> NotificationService:
    return request.app.state.notification_service


def get_admin_service(request: Request) -> NotificationService:
    return request.app.state.admin_service


def get_current_user(
    token: TokenDep,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.jwt_token.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    username = token_data.sub
    if not username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = user_service.get_by_username(username)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_user_profile(
    user_profile_service: Annotated[
        UserProfileService, Depends(get_user_profile_service)
    ],
    current_user: CurrentUser,
) -> UserProfile:
    user_profile = user_profile_service.get_by_user_id(
        user_id=current_user.id,
    )

    if not user_profile:
        raise UserProfileNotFoundError()

    return user_profile


def get_current_active_admin(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )

    return current_user


AdminUser = Annotated[User, Depends(get_current_active_admin)]
