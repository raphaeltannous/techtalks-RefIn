import uuid

from models.user_language import (
    UserLanguage,
    UserLanguageIn,
    UserLanguagePublic,
    UserLanguagesPublic,
    UserLanguageUpdate,
)
from repositories.user import UserRepository
from repositories.user_language import UserLanguageRepository
from repositories.user_profile import UserProfileRepository


class UserLanguageService:
    def __init__(
        self,
        *,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        user_language_repository: UserLanguageRepository,
    ):
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository
        self.user_language_repository = user_language_repository

    def get_all_by_username(
        self,
        *,
        username: str,
    ) -> UserLanguagesPublic:
        user = self.user_repository.get_by_username(
            username=username,
        )

        user_profile = self.user_profile_repository.get_by_user_id(
            user_id=user.id,
        )

        languages = self.user_language_repository.get_all_by_user_profile_id(
            user_profile.id,
        )

        public_languages = [
            UserLanguagePublic.model_validate(language) for language in languages
        ]

        return UserLanguagesPublic(
            languages=public_languages,
        )

    def get_by_id(
        self,
        *,
        language_id: uuid.UUID,
    ) -> UserLanguagePublic:
        language = self.user_language_repository.get_by_id(
            language_id=language_id,
        )

        return UserLanguagePublic.model_validate(
            language,
        )

    def add(
        self,
        *,
        profile_id: uuid.UUID,
        language_in: UserLanguageIn,
    ) -> UserLanguagePublic:
        user_profile = self.user_profile_repository.get_by_id(
            profile_id=profile_id,
        )

        language = UserLanguage.model_validate(
            language_in,
            update={
                "user_profile_id": user_profile.id,
            },
        )

        language = self.user_language_repository.add(
            language,
        )

        return UserLanguagePublic.model_validate(
            language,
        )

    def update(
        self,
        *,
        language_id: uuid.UUID,
        language_in: UserLanguageUpdate,
    ) -> UserLanguagePublic:
        language = self.user_language_repository.get_by_id(
            language_id=language_id,
        )

        language = self.user_language_repository.update(
            language_db=language,
            language_in=language_in,
        )

        return UserLanguagePublic.model_validate(
            language,
        )

    def delete(
        self,
        *,
        language_id: uuid.UUID,
    ) -> None:
        language = self.user_language_repository.get_by_id(
            language_id=language_id,
        )

        self.user_language_repository.delete(
            language_db=language,
        )
