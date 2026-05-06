import uuid

from exceptions import UserProfileNotFoundError
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
    ) -> UserProfile:
        with Session(self.engine) as session:
            profile = session.get(UserProfile, profile_id)

            if profile is None:
                raise UserProfileNotFoundError()

            return profile

    def get_by_user_id(
        self,
        user_id: uuid.UUID,
    ) -> UserProfile:
        with Session(self.engine) as session:
            statement = select(UserProfile).where(UserProfile.user_id == user_id)

            profile = session.exec(statement).first()

            if profile is None:
                raise UserProfileNotFoundError()

            return profile

    def update_profile_picture(
        self,
        profile_db: UserProfile,
        filename: str,
    ) -> UserProfile:
        with Session(self.engine) as session:
            profile_db.profile_picture = filename

            session.add(profile_db)
            session.commit()
            session.refresh(profile_db)

            return profile_db

    def update_banner(
        self,
        profile_db: UserProfile,
        filename: str,
    ) -> UserProfile:
        with Session(self.engine) as session:
            profile_db.banner = filename

            session.add(profile_db)
            session.commit()
            session.refresh(profile_db)

            return profile_db

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
