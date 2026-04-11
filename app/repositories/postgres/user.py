import uuid

from models.user import User
from pydantic import EmailStr
from repositories.user import UserRepository
from sqlmodel import Session, select


class PostgresUserRepository(UserRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        with Session(self.engine) as session:
            return session.get(User, user_id)

    def get_by_email(self, user_email: EmailStr) -> User | None:
        statement = select(User).where(User.email == user_email)
        user = self.db.exec(statement).first()
        return user
