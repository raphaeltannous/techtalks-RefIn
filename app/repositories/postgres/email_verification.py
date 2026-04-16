from sqlmodel import Session, select

from app.models.email_verification import EmailVerification, EmailVerificationUpdate
from app.repositories.email_verification import AbstractEmailVerificationRepository


class PostgresEmailVerificationRepository(AbstractEmailVerificationRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_token_hash(self, token_hash: str) -> EmailVerification | None:
        statement = select(EmailVerification).where(
            EmailVerification.token_hash == token_hash
        )
        return self.session.exec(statement).first()

    def update(
        self,
        db_obj: EmailVerification,
        obj_in: EmailVerificationUpdate,
    ) -> EmailVerification:
        update_data = obj_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)

        return db_obj