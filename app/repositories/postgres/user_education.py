import uuid
from typing import Sequence

from models.user_education import UserEducation, UserEducationUpdate
from repositories.user_education import UserEducationRepository
from sqlmodel import Session, col, select


class PostgresUserEducationRepository(UserEducationRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_all_by_user_profile_id(
        self,
        user_profile_id: uuid.UUID,
    ) -> Sequence[UserEducation]:
        with Session(self.engine) as session:
            statement = (
                select(UserEducation)
                .order_by(col(UserEducation.created_at).desc())
                .where(UserEducation.user_profile_id == user_profile_id)
            )

            user_educations = session.exec(statement).all()

            return user_educations

    def get_by_id(
        self,
        education_id: uuid.UUID,
    ) -> UserEducation | None:
        with Session(self.engine) as session:
            return session.get(UserEducation, education_id)

    def add(
        self,
        education_in: UserEducation,
    ) -> UserEducation:
        with Session(self.engine) as session:
            session.add(education_in)
            session.commit()
            session.refresh(education_in)

            return education_in

    def update(
        self,
        education_db: UserEducation,
        education_in: UserEducationUpdate,
    ) -> UserEducation:
        with Session(self.engine) as session:
            update_data = education_in.model_dump(
                exclude_unset=True,
            )

            education_db.sqlmodel_update(update_data)
            session.add(education_db)
            session.commit()
            session.refresh(education_db)

            return education_db

    def delete(
        self,
        education_db: UserEducation,
    ) -> None:
        with Session(self.engine) as session:
            session.delete(education_db)
            session.commit()
