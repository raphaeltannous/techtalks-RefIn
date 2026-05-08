import security.password_hashing
from config import settings
from exceptions import DuplicateUserError
from models.user import User
from services.user import UserService


def init(
    user_service: UserService,
) -> None:
    try:
        admin_user = User(
            username=settings.FIRST_ADMIN_USERNAME,
            email=settings.FIRST_ADMIN_EMAIL,
            hashed_password=security.password_hashing.get_password_hash(
                settings.FIRST_ADMIN_PASSWORD,
            ),
            is_active=True,
            is_verified=True,
        )

        admin_user = user_service.add(
            user_in=admin_user,
        )
    except DuplicateUserError:
        pass
