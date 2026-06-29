from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.identity.client_profile import ClientProfile
from app.models.identity.organization_member import OrganizationMember
from app.models.identity.refresh_token import RefreshToken
from app.models.identity.role import Role
from app.models.identity.user import User


class ClientRepository:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Users
    # -------------------------

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = select(User).where(
            User.email == email.lower()
        )

        return self.db.scalar(statement)

    def create_user(
        self,
        user: User,
    ) -> User:

        self.db.add(user)
        self.db.flush()
        return user

    # -------------------------
    # Client Profile
    # -------------------------

    def create_client_profile(
        self,
        profile: ClientProfile,
    ) -> ClientProfile:

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
    # Roles
    # -------------------------

    def get_role_by_name(
        self,
        name: str,
    ) -> Role | None:

        statement = select(Role).where(
            Role.name == name
        )

        return self.db.scalar(statement)

    # -------------------------
    # Transactions
    # -------------------------

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()