from abc import ABC, abstractmethod
from uuid import UUID

from app.models.email_verification import EmailVerification, EmailVerificationUpdate


class AbstractEmailVerificationRepository(ABC):

    @abstractmethod
    def get_by_token_hash(self, token_hash: str) -> EmailVerification | None:
        """Fetch verification record using hashed token."""
        ...

    @abstractmethod
    def update(
        self,
        db_obj: EmailVerification,
        obj_in: EmailVerificationUpdate,
    ) -> EmailVerification:
        """Update email verification record."""
        ...