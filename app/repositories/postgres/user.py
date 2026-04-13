import uuid
from typing import Sequence

from models.user import User
from pydantic import EmailStr
from repositories.user import UserRepository
from sqlmodel import Session, col, func, select
from security.password_hashing import get_password_hash

class PostgresUserRepository(UserRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_users(self, offset: int, limit: int) -> tuple[Sequence[User], int]:
        with Session(self.engine) as session:
            count_statement = select(func.count()).select_from(User)
            count = session.exec(count_statement).one()

            statement = (
                select(User)
                .order_by(col(User.created_at).desc())
                .offset(offset)
                .limit(limit)
            )

            users = session.exec(statement).all()

            return users, count

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        with Session(self.engine) as session:
            return session.get(User, user_id)

    def get_by_email(self, user_email: EmailStr) -> User | None:
        with Session(self.engine) as session:
            statement = select(User).where(User.email == user_email)
            user = session.exec(statement).first()

            return user
        
    def create_user(self, email: EmailStr, password: str, is_admin: bool) -> User:
        with Session(self.engine) as session:
            user = User(
                email=email,
                name=None,
                hashed_password=get_password_hash(password),
                is_admin=is_admin,
                is_active=True,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return user
