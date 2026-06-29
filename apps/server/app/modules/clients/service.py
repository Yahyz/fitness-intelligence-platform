from sqlalchemy.orm import Session

from app.builders import (
    build_client_profile,
    build_membership,
    build_user,
)
from app.core.passwords import generate_temporary_password
from app.core.security import hash_password
from app.modules.clients.repository import ClientRepository
from app.modules.clients.schemas import (
    ClientResponse,
    CreateClientRequest,
)
from app.core.exceptions import (
    ClientAlreadyExistsError,
    ClientRoleNotFoundError,
)


class ClientService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.repository = ClientRepository(db)

    def create_client(
        self,
        request: CreateClientRequest,
        current_user,
    ) -> ClientResponse:

        # --------------------------------
        # Email already exists?
        # --------------------------------

        if self.repository.get_user_by_email(
            request.email
        ):
            raise ClientAlreadyExistsError(
    "Email already exists."
)

        # --------------------------------
        # Get Client role
        # --------------------------------

        client_role = self.repository.get_role_by_name(
            "Client"
        )

        if client_role is None:
            raise ClientRoleNotFoundError(
    "Client role not found."
)

        # --------------------------------
        # Organization
        # --------------------------------

        organization = (
            current_user.organization_memberships[0]
            .organization
        )

        # --------------------------------
        # Temporary password
        # --------------------------------

        temporary_password = (
            generate_temporary_password()
        )

        password_hash = hash_password(
            temporary_password
        )

        # --------------------------------
        # User
        # --------------------------------

        user = build_user(
            email=request.email,
            password_hash=password_hash,
        )

        user = self.repository.create_user(
            user
        )

        # --------------------------------
        # Client profile
        # --------------------------------

        profile = build_client_profile(
            user_id=user.id,
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone,
        )

        self.repository.create_client_profile(
            profile
        )

        # --------------------------------
        # Membership
        # --------------------------------

        membership = build_membership(
            organization_id=organization.id,
            user_id=user.id,
            role_id=client_role.id,
        )

        self.repository.create_membership(
            membership
        )

        self.repository.commit()

        return ClientResponse(
            id=user.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            email=user.email,
            phone=profile.phone,
            is_active=user.is_active,
        )