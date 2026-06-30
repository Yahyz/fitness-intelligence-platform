from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.identity.client_profile import ClientProfile
from app.models.identity.organization_member import OrganizationMember
from app.models.identity.refresh_token import RefreshToken
from app.models.identity.role import Role
from app.models.identity.user import User
from sqlalchemy.orm import joinedload
from uuid import UUID

from app.models.identity.client_profile import ClientProfile
from app.models.identity.organization_member import OrganizationMember


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

    def get_clients_by_organization(
        self,
        organization_id,
    ) -> list[OrganizationMember]:

        statement = (
            select(OrganizationMember)
            .options(
                joinedload(OrganizationMember.user)
                .joinedload(User.client_profile)
        )
            .where(
                OrganizationMember.organization_id == organization_id
        )
            .join(Role)
            .where(Role.name == "Client")
    )

        return list(self.db.scalars(statement).all())
    
    def get_client_by_id(
    self,
    client_id: UUID | str,
    organization_id,
    ) -> OrganizationMember | None:

        statement = (
            select(OrganizationMember)
            .options(
                joinedload(OrganizationMember.user)
                .joinedload(User.client_profile)
            )
            .join(OrganizationMember.role)
            .where(
                OrganizationMember.user_id == client_id,
                OrganizationMember.organization_id == organization_id,
                Role.name == "Client",
        )
    )

        return self.db.scalar(statement)
    
    def update_client_profile(
    self,
    profile: ClientProfile,
    ):
        self.db.flush()
        return profile
    
    def deactivate_user(
    self,
    user: User,
) -> User:

        user.is_active = False

        self.db.flush()

        return user