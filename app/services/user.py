from models.user import User
from pydantic import EmailStr
from repositories.user import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def get_by_email(self, email: EmailStr) -> User | None:
        pass
