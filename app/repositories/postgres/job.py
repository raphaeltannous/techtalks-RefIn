import uuid
from typing import Sequence

from models.job import Job, JobUpdate
from repositories.job import JobRepository
from sqlmodel import Session, col, func, select

from app.exceptions import JobNotFoundError


class PostgresJobRepository(JobRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_all(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Job], int]:
        with Session(self.engine) as session:
            count_statement = select(func.count()).select_from(Job)
            count = session.exec(count_statement).one()

            statement = (
                select(Job)
                .order_by(col(Job.created_at).desc())
                .offset(offset)
                .limit(limit)
            )

            jobs = session.exec(statement).all()

            return jobs, count

    def get_all_by_user_id(
        self,
        user_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Job], int]:
        with Session(self.engine) as session:
            count_statement = (
                select(func.count()).select_from(Job).where(Job.user_id == user_id)
            )
            count = session.exec(count_statement).one()

            statement = (
                select(Job)
                .order_by(col(Job.created_at).desc())
                .where(Job.user_id == user_id)
                .offset(offset)
                .limit(limit)
            )

            jobs = session.exec(statement).all()

            return jobs, count

    def get_by_id(
        self,
        job_id: uuid.UUID,
    ) -> Job:
        """
        Will raise UserNotFoundError() when not found.
        """
        with Session(self.engine) as session:
            job = session.get(Job, job_id)

            if job is None:
                raise JobNotFoundError()

            return job

    def add(
        self,
        job_in: Job,
    ) -> Job:
        with Session(self.engine) as session:
            session.add(job_in)
            session.commit()
            session.refresh(job_in)

            return job_in

    def update(
        self,
        job_db: Job,
        job_in: JobUpdate,
    ) -> Job:
        with Session(self.engine) as session:
            update_data = job_in.model_dump(
                exclude_unset=True,
            )

            job_db.sqlmodel_update(update_data)
            session.add(job_db)
            session.commit()
            session.refresh(job_db)

            return job_db

    def delete(
        self,
        job_db: Job,
    ) -> None:
        with Session(self.engine) as session:
            session.delete(job_db)
            session.commit()
