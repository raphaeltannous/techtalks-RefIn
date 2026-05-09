import uuid
from typing import Sequence

from exceptions import JobNationalityNotFoundError
from models.job_nationality import JobNationality, JobNationalityUpdate
from repositories.job_nationality import JobNationalityRepository
from sqlmodel import Session, col, select


class PostgresJobNationalityRepository(JobNationalityRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_all_by_job_id(
        self,
        job_id: uuid.UUID,
    ) -> Sequence[JobNationality]:
        with Session(self.engine) as session:
            statement = (
                select(JobNationality)
                .order_by(col(JobNationality.created_at).desc())
                .where(JobNationality.job_id == job_id)
            )
            nationalities = session.exec(statement).all()

            return nationalities

    def get_by_id(
        self,
        nationality_id: uuid.UUID,
    ) -> JobNationality:
        with Session(self.engine) as session:
            nationality = session.get(JobNationality, nationality_id)

            if nationality is None:
                raise JobNationalityNotFoundError()

            return nationality

    def add(
        self,
        nationality_in: JobNationality,
    ) -> JobNationality:
        with Session(self.engine) as session:
            session.add(nationality_in)
            session.commit()
            session.refresh(nationality_in)

            return nationality_in

    def update(
        self,
        nationality_db: JobNationality,
        nationality_in: JobNationalityUpdate,
    ) -> JobNationality:
        with Session(self.engine) as session:
            update_data = nationality_in.model_dump(
                exclude_unset=True,
            )

            nationality_db.sqlmodel_update(update_data)
            session.add(nationality_db)
            session.commit()
            session.refresh(nationality_db)

            return nationality_db

    def delete(
        self,
        nationality_db: JobNationality,
    ) -> None:
        with Session(self.engine) as session:
            session.delete(nationality_db)
            session.commit()
