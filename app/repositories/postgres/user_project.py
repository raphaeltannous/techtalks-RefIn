import uuid
from typing import Sequence

from models.user_project import UserProject, UserProjectUpdate
from repositories.user_project import UserProjectRepository
from sqlmodel import Session, col, select


class PostgresUserProjectRepository(UserProjectRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_all_by_user_profile_id(
        self,
        user_profile_id: uuid.UUID,
    ) -> Sequence[UserProject]:
        with Session(self.engine) as session:
            statement = (
                select(UserProject)
                .order_by(col(UserProject.created_at).desc())
                .where(UserProject.user_profile_id == user_profile_id)
            )

            user_projects = session.exec(statement).all()

            return user_projects

    def get_by_id(
        self,
        project_id: uuid.UUID,
    ) -> UserProject | None:
        with Session(self.engine) as session:
            return session.get(UserProject, project_id)

    def add(
        self,
        project_in: UserProject,
    ) -> UserProject:
        with Session(self.engine) as session:
            session.add(project_in)
            session.commit()
            session.refresh(project_in)

            return project_in

    def update(
        self,
        project_db: UserProject,
        project_in: UserProjectUpdate,
    ) -> UserProject:
        with Session(self.engine) as session:
            update_data = project_in.model_dump(
                exclude_unset=True,
            )

            project_db.sqlmodel_update(update_data)
            session.add(project_db)
            session.commit()
            session.refresh(project_db)

            return project_db

    def delete(
        self,
        project_db: UserProject,
    ) -> None:
        with Session(self.engine) as session:
            session.delete(project_db)
            session.commit()
