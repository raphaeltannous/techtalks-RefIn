from repositories.job import JobRepository
from repositories.job_application import JobApplicationRepository
from repositories.job_language import JobLanguageRepository
from repositories.job_nationality import JobNationalityRepository
from repositories.notification import NotificationRepository
from repositories.user import UserRepository
from repositories.user_certificate import UserCertificateRepository
from repositories.user_education import UserEducationRepository
from repositories.user_experience import UserExperienceRepository
from repositories.user_language import UserLanguageRepository
from repositories.user_link import UserLinkRepository
from repositories.user_profile import UserProfileRepository
from repositories.user_project import UserProjectRepository
from repositories.user_skill import UserSkillRepository

from ._admin.job import JobService
from ._admin.user import UserService
from ._admin.user_profile import UserProfileService


class AdminService:
    def __init__(
        self,
        *,
        user_repository: UserRepository,
        user_skill_repository: UserSkillRepository,
        user_profile_repository: UserProfileRepository,
        user_language_repository: UserLanguageRepository,
        user_link_repository: UserLinkRepository,
        user_experience_repository: UserExperienceRepository,
        user_project_repository: UserProjectRepository,
        user_education_repository: UserEducationRepository,
        user_certificate_repository: UserCertificateRepository,
        job_repository: JobRepository,
        job_language_repository: JobLanguageRepository,
        job_application_repository: JobApplicationRepository,
        job_nationality_repository: JobNationalityRepository,
        notification_repository: NotificationRepository,
    ):

        self.user_service = UserService(
            user_repository=user_repository,
        )
        self.job_service = JobService(
            user_repository=user_repository,
            job_repository=job_repository,
            job_language_repository=job_language_repository,
            job_application_repository=job_application_repository,
            job_nationality_repository=job_nationality_repository,
            notification_repository=notification_repository,
        )
        self.user_profile_service = UserProfileService(
            user_repository=user_repository,
            user_skill_repository=user_skill_repository,
            user_profile_repository=user_profile_repository,
            user_language_repository=user_language_repository,
            user_link_repository=user_link_repository,
            user_project_repository=user_project_repository,
            user_certificate_repository=user_certificate_repository,
            user_experience_repository=user_experience_repository,
            user_education_repository=user_education_repository,
        )
