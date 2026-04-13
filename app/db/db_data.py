from services.user import UserService
from config import settings


def init(user_service: UserService) -> None:
    # Check if database is empty (no users at all)
    _, user_count = user_service.get_private_users(offset=0, limit=1)
    
    # Create admin only if database has no users
    if user_count == 0:
        user_service.create_user(
            email=settings.FIRST_ADMIN_EMAIL,
            password=settings.FIRST_ADMIN_PASSWORD,
            is_admin=True,
        )
    return
'''
def init(
    user_service: UserService,
) -> None:
    # TODO: Check if FIRST_ADMIN_EMAIL exists in db.
    # TODO: Create if not.

    # with Session(engine) as session:
    #     user = session.exec(
    #         select(User).where(User.email == settings.FIRST_ADMIN_EMAIL)
    #     ).first()
    #     if not user:
    #         user_in = UserCreate(
    #             email=settings.FIRST_ADMIN_EMAIL,
    #             password=settings.FIRST_ADMIN_PASSWORD,
    #             is_admin=True,
    #         )
    #         # Use UserService
    #         user = crud.users.create_user(session=session, user_create=user_in)
    return
'''