import uuid
from abc import ABCMeta, abstractmethod
from typing import Sequence

from models.user_certificate import UserCertificate, UserCertificateUpdate


class UserCertificateRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_by_user_profile_id(
        self,
        user_profile_id: uuid.UUID,
    ) -> Sequence[UserCertificate]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        certificate_id: uuid.UUID,
    ) -> UserCertificate:
        """
        Will raise UserCertificateNotFoundError() when not found.
        """
        pass

    @abstractmethod
    def add(
        self,
        certificate_in: UserCertificate,
    ) -> UserCertificate:
        pass

    @abstractmethod
    def update(
        self,
        certificate_db: UserCertificate,
        certificate_in: UserCertificateUpdate,
    ) -> UserCertificate:
        pass

    @abstractmethod
    def delete(
        self,
        certificate_db: UserCertificate,
    ) -> None:
        pass
