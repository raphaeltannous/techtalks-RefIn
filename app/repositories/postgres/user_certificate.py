import uuid
from typing import Sequence

from exceptions import UserCertificateNotFoundError
from models.user_certificate import UserCertificate, UserCertificateUpdate
from repositories.user_certificate import UserCertificateRepository
from sqlmodel import Session, col, select


class PostgresUserCertificateRepository(UserCertificateRepository):
    def __init__(
        self,
        engine,
    ) -> None:
        self.engine = engine

    def get_all_by_user_profile_id(
        self,
        user_profile_id: uuid.UUID,
    ) -> Sequence[UserCertificate]:
        with Session(self.engine) as session:
            statement = (
                select(UserCertificate)
                .order_by(col(UserCertificate.created_at).desc())
                .where(UserCertificate.user_profile_id == user_profile_id)
            )

            user_certificates = session.exec(statement).all()

            return user_certificates

    def get_by_id(
        self,
        certificate_id: uuid.UUID,
    ) -> UserCertificate:
        with Session(self.engine) as session:
            certificate = session.get(UserCertificate, certificate_id)

            if certificate is None:
                raise UserCertificateNotFoundError()

            return certificate

    def add(
        self,
        certificate_in: UserCertificate,
    ) -> UserCertificate:
        with Session(self.engine) as session:
            session.add(certificate_in)
            session.commit()
            session.refresh(certificate_in)

            return certificate_in

    def update(
        self,
        certificate_db: UserCertificate,
        certificate_in: UserCertificateUpdate,
    ) -> UserCertificate:
        with Session(self.engine) as session:
            update_data = certificate_in.model_dump(
                exclude_unset=True,
            )

            certificate_db.sqlmodel_update(update_data)
            session.add(certificate_db)
            session.commit()
            session.refresh(certificate_db)

            return certificate_db

    def delete(
        self,
        certificate_db: UserCertificate,
    ) -> None:
        with Session(self.engine) as session:
            session.delete(certificate_db)
            session.commit()
