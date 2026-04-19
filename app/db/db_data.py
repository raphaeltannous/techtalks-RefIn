import security.password_hashing
from config import settings
from models.user import User
from services.user import UserService


def init(
    user_service: UserService,
) -> None:
    _, count = user_service.get_private_users(offset=0, limit=1)

    if count == 0:
        user = User(
            email=settings.FIRST_ADMIN_EMAIL,
            name=settings.FIRST_ADMIN_NAME,
            is_admin=True,
            is_active=True,
            hashed_password=security.password_hashing.get_password_hash(
                settings.FIRST_ADMIN_PASSWORD,
            ),
        )

        user_service.user_repository.add_user(user)
