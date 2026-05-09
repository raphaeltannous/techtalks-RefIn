import uuid
from typing import Sequence

from exceptions import JobLanguageNotFoundError
from models.job_language import JobLanguage, JobLanguageUpdate
from repositories.job_language import JobLanguageRepository
from sqlmodel import Session, col, select


class PostgresJobLanguageRepository(JobLanguageRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_all_by_job_id(
        self,
        job_id: uuid.UUID,
    ) -> Sequence[JobLanguage]:
        with Session(self.engine) as session:
            statement = (
                select(JobLanguage)
                .order_by(col(JobLanguage.created_at).desc())
                .where(JobLanguage.job_id == job_id)
            )
            languages = session.exec(statement).all()

            return languages

    def get_by_id(
        self,
        language_id: uuid.UUID,
    ) -> JobLanguage:
        with Session(self.engine) as session:
            language = session.get(JobLanguage, language_id)

            if language is None:
                raise JobLanguageNotFoundError()

            return language

    def add(
        self,
        language_in: JobLanguage,
    ) -> JobLanguage:
        with Session(self.engine) as session:
            session.add(language_in)
            session.commit()
            session.refresh(language_in)

            return language_in

    def update(
        self,
        language_db: JobLanguage,
        language_in: JobLanguageUpdate,
    ) -> JobLanguage:
        with Session(self.engine) as session:
            update_data = language_in.model_dump(
                exclude_unset=True,
            )

            language_db.sqlmodel_update(update_data)
            session.add(language_db)
            session.commit()
            session.refresh(language_db)

            return language_db

    def delete(
        self,
        language_db: JobLanguage,
    ) -> None:
        with Session(self.engine) as session:
            session.delete(language_db)
            session.commit()
