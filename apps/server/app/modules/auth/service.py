from sqlalchemy.orm import Session

from app.builders import (
    build_coach_profile,
    build_membership,
    build_organization,
    build_organization_settings,
    build_refresh_token,
    build_user,
)
from app.core.exceptions import (
    EmailAlreadyExistsError,
    RoleNotFoundError,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    RegisterOrganizationRequest,
    TokenResponse,
    AuthUserResponse,
)
from app.shared.slug import generate_unique_slug
from app.core.security import hash_password

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
)

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AuthRepository(db)

    def register_organization(
        self,
        request: RegisterOrganizationRequest,
    ) -> TokenResponse:
        """
        Register a new organization and its owner.
        Commit 1: Validation only.
        """

        # -----------------------------
        # Validate email
        # -----------------------------
        if self.repository.email_exists(request.email):
            raise EmailAlreadyExistsError(
                f"Email '{request.email}' is already registered."
            )

        # -----------------------------
        # Validate Owner role
        # -----------------------------
        owner_role = self.repository.get_role_by_name("Owner")

        if owner_role is None:
            raise RoleNotFoundError(
                "Owner role not found."
            )

        # -----------------------------
        # Generate organization slug
        # -----------------------------
        slug = generate_unique_slug(
            request.organization_name,
            self.repository,
        )

               # -----------------------------
        # Hash password
        # -----------------------------

        password_hash = hash_password(
            request.password
        )

        # -----------------------------
        # Create Organization
        # -----------------------------

        organization = build_organization(
            name=request.organization_name,
            slug=slug,
        )

        organization = self.repository.create_organization(
            organization
        )

        # -----------------------------
        # Create Organization Settings
        # -----------------------------

        organization_settings = build_organization_settings(
            organization.id
        )

        self.repository.create_organization_settings(
            organization_settings
        )

        # -----------------------------
        # Create User
        # -----------------------------

        user = build_user(
            email=request.email,
            password_hash=password_hash,
        )

        user = self.repository.create_user(
            user
        )

        # -----------------------------
        # Create Coach Profile
        # -----------------------------

        coach_profile = build_coach_profile(
            user_id=user.id,
            first_name=request.owner_first_name,
            last_name=request.owner_last_name,
            phone=request.phone,
        )

        self.repository.create_coach_profile(
            coach_profile
        )

        # -----------------------------
        # Create Membership
        # -----------------------------

        membership = build_membership(
            organization_id=organization.id,
            user_id=user.id,
            role_id=owner_role.id,
        )

        self.repository.create_membership(
            membership
        )

        # -----------------------------
        # Generate tokens
        # -----------------------------

        access_token = create_access_token(
            subject=str(user.id),
        )

        refresh_token_value = create_refresh_token()

        refresh_token = build_refresh_token(
            user_id=user.id,
            token=refresh_token_value,
        )

        self.repository.create_refresh_token(
            refresh_token
        )

        # -----------------------------
        # Commit transaction
        # -----------------------------

        self.repository.commit()

        # -----------------------------
        # Return response
        # -----------------------------

        return TokenResponse(
    access_token=access_token,
    refresh_token=refresh_token_value,
    user=AuthUserResponse(
        id=str(user.id),
        email=user.email,
        first_name=coach_profile.first_name,
        last_name=coach_profile.last_name,
        organization=organization.name,
        role=owner_role.name,
    ),
)
