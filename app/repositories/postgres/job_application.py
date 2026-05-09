import uuid
from typing import Sequence

from exceptions import JobApplicationNotFoundError
from models.job_application import JobApplication, JobApplicationUpdate
from repositories.job_application import JobApplicationRepository
from sqlmodel import Session, col, select


class PostgresJobApplicationRepository(JobApplicationRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_all_by_job_id(
        self,
        job_id: uuid.UUID,
    ) -> Sequence[JobApplication]:
        with Session(self.engine) as session:
            statement = (
                select(JobApplication)
                .order_by(col(JobApplication.created_at).desc())
                .where(JobApplication.job_id == job_id)
            )
            applications = session.exec(statement).all()

            return applications

    def get_all_by_user_id(
        self,
        user_id: uuid.UUID,
    ) -> Sequence[JobApplication]:
        with Session(self.engine) as session:
            statement = (
                select(JobApplication)
                .order_by(col(JobApplication.created_at).desc())
                .where(JobApplication.user_id == user_id)
            )
            applications = session.exec(statement).all()

            return applications

    def get_by_user_id_and_job_id(
        self,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> JobApplication:
        with Session(self.engine) as session:
            statement = (
                select(JobApplication)
                .order_by(col(JobApplication.created_at).desc())
                .where(
                    (JobApplication.user_id == user_id)
                    & (JobApplication.job_id == job_id)
                )
            )

            application = session.exec(statement).first()

            if application is None:
                raise JobApplicationNotFoundError()

            return application

    def get_by_id(
        self,
        application_id: uuid.UUID,
    ) -> JobApplication:
        with Session(self.engine) as session:
            application = session.get(JobApplication, application_id)

            if application is None:
                raise JobApplicationNotFoundError()

            return application

    def add(
        self,
        application_in: JobApplication,
    ) -> JobApplication:
        with Session(self.engine) as session:
            session.add(application_in)
            session.commit()
            session.refresh(application_in)

            return application_in

    def update(
        self,
        application_db: JobApplication,
        application_in: JobApplicationUpdate,
    ) -> JobApplication:
        with Session(self.engine) as session:
            update_data = application_in.model_dump(
                exclude_unset=True,
            )

            application_db.sqlmodel_update(update_data)
            session.add(application_db)
            session.commit()
            session.refresh(application_db)

            return application_db

    def delete(
        self,
        application_db: JobApplication,
    ) -> None:
        with Session(self.engine) as session:
            session.delete(application_db)
            session.commit()
