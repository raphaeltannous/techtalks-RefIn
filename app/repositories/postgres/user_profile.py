import uuid

from models.user_profile import UserProfile, UserProfileUpdate
from repositories.user_profile import UserProfileRepository
from sqlmodel import Session, select


class PostgresUserProfileRepository(UserProfileRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_by_id(
        self,
        profile_id: uuid.UUID,
    ) -> UserProfile | None:
        with Session(self.engine) as session:
            return session.get(UserProfile, profile_id)

    def get_by_user_id(
        self,
        user_id: uuid.UUID,
    ) -> UserProfile | None:
        with Session(self.engine) as session:
            statement = select(UserProfile).where(UserProfile.user_id == user_id)

            user_profile = session.exec(statement).first()

            return user_profile

    def update(
        self,
        profile_db: UserProfile,
        profile_in: UserProfileUpdate,
    ) -> UserProfile:
        with Session(self.engine) as session:
            update_data = profile_in.model_dump(
                exclude_unset=True,
            )

            profile_db.sqlmodel_update(update_data)
            session.add(profile_db)
            session.commit()
            session.refresh(profile_db)

            return profile_db
