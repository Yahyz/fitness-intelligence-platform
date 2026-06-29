from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.identity.coach_profile import CoachProfile
from app.models.identity.organization import Organization
from app.models.identity.organization_member import OrganizationMember
from app.models.identity.organization_settings import OrganizationSettings
from app.models.identity.refresh_token import RefreshToken
from app.models.identity.role import Role
from app.models.identity.user import User
from datetime import datetime
from uuid import UUID

class AuthRepository:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Users
    # -------------------------

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(
            User.email == email.lower()
        )
        return self.db.scalar(statement)

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user

    def email_exists(self, email: str) -> bool:
        return self.get_user_by_email(email) is not None
    # -------------------------
    # Roles
    # -------------------------

    def get_role_by_name(self, name: str) -> Role | None:
        statement = select(Role).where(Role.name == name)
        return self.db.scalar(statement)

    # -------------------------
    # Organizations
    # -------------------------

    def create_organization(
        self,
        organization: Organization,
    ) -> Organization:

        self.db.add(organization)
        self.db.flush()
        return organization

    def slug_exists(self, slug: str) -> bool:
        statement = select(Organization).where(
            Organization.slug == slug
        )
        return self.db.scalar(statement) is not None

    # -------------------------
    # Organization Settings
    # -------------------------

    def create_organization_settings(
        self,
        settings: OrganizationSettings,
    ) -> OrganizationSettings:

        self.db.add(settings)
        self.db.flush()
        return settings

    # -------------------------
    # Coach Profile
    # -------------------------

    def create_coach_profile(
        self,
        profile: CoachProfile,
    ) -> CoachProfile:

        self.db.add(profile)
        self.db.flush()
        return profile

    # -------------------------
    # Membership
    # -------------------------

    def create_membership(
        self,
        membership: OrganizationMember,
    ) -> OrganizationMember:

        self.db.add(membership)
        self.db.flush()
        return membership

    # -------------------------
    # Refresh Token
    # -------------------------

    def create_refresh_token(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:

        self.db.add(refresh_token)
        self.db.flush()
        return refresh_token
    
    def update_last_login(
    self,
    user: User,
    ):
     user.last_login = datetime.utcnow()
     self.db.flush()

    # -------------------------
    # Transactions
    # -------------------------

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def get_role_by_id(self, role_id: int) -> Role | None:
        statement = select(Role).where(
        Role.id == role_id
    )
        return self.db.scalar(statement)
    def get_user_by_id(
    self,
    user_id: UUID | str,
) -> User | None:

        statement = select(User).where(
        User.id == user_id
    )

        return self.db.scalar(statement)