from services.user import UserService


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
