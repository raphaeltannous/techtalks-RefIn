import uuid

from exceptions import ForbiddenAction
from models.user_certificate import (
    UserCertificate,
    UserCertificateIn,
    UserCertificatePublic,
    UserCertificatesPublic,
    UserCertificateUpdate,
)
from models.user_profile import UserProfile
from repositories.user import UserRepository
from repositories.user_certificate import UserCertificateRepository
from repositories.user_profile import UserProfileRepository


class UserCertificateService:
    def __init__(
        self,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        user_certificate_repository: UserCertificateRepository,
    ):
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository
        self.user_certificate_repository = user_certificate_repository

    def get_all_by_username(
        self,
        *,
        username: str,
    ) -> UserCertificatesPublic:
        user = self.user_repository.get_by_username(
            username=username,
        )

        user_profile = self.user_profile_repository.get_by_user_id(
            user_id=user.id,
        )

        certificates = self.user_certificate_repository.get_all_by_user_profile_id(
            user_profile.id,
        )

        public_certificates = [
            UserCertificatePublic.model_validate(certificate)
            for certificate in certificates
        ]

        return UserCertificatesPublic(
            certificates=public_certificates,
        )

    def get_by_id(
        self,
        *,
        certificate_id: uuid.UUID,
    ) -> UserCertificatePublic:
        certificate = self.user_certificate_repository.get_by_id(
            certificate_id=certificate_id,
        )

        return UserCertificatePublic.model_validate(
            certificate,
        )

    def add(
        self,
        *,
        user_profile: UserProfile,
        certificate_in: UserCertificateIn,
    ) -> UserCertificatePublic:
        certificate = UserCertificate.model_validate(
            certificate_in,
            update={
                "user_profile_id": user_profile.id,
            },
        )

        certificate = self.user_certificate_repository.add(
            certificate,
        )

        return UserCertificatePublic.model_validate(
            certificate,
        )

    def update(
        self,
        *,
        user_profile: UserProfile,
        certificate_id: uuid.UUID,
        certificate_in: UserCertificateUpdate,
    ) -> UserCertificatePublic:
        certificate = self.user_certificate_repository.get_by_id(
            certificate_id=certificate_id,
        )

        if certificate.user_profile_id != user_profile.id:
            raise ForbiddenAction()

        certificate = self.user_certificate_repository.update(
            certificate_db=certificate,
            certificate_in=certificate_in,
        )

        return UserCertificatePublic.model_validate(
            certificate,
        )

    def delete(
        self,
        *,
        user_profile: UserProfile,
        certificate_id: uuid.UUID,
    ) -> None:
        certificate = self.user_certificate_repository.get_by_id(
            certificate_id=certificate_id,
        )

        if certificate.user_profile_id != user_profile.id:
            raise ForbiddenAction()

        self.user_certificate_repository.delete(
            certificate_db=certificate,
        )
