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
    InvalidCredentialsError,
    InactiveUserError,
    RoleNotFoundError,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    AuthUserResponse,
    LoginRequest,
    RegisterOrganizationRequest,
    TokenResponse,
)
from app.shared.slug import generate_unique_slug


class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = AuthRepository(db)

    def register_organization(
        self,
        request: RegisterOrganizationRequest,
    ) -> TokenResponse:

        if self.repository.email_exists(request.email):
            raise EmailAlreadyExistsError(
                f"Email '{request.email}' is already registered."
            )

        owner_role = self.repository.get_role_by_name(
            "Owner"
        )

        if owner_role is None:
            raise RoleNotFoundError(
                "Owner role not found."
            )

        slug = generate_unique_slug(
            request.organization_name,
            self.repository,
        )

        password_hash = hash_password(
            request.password
        )

        organization = build_organization(
            name=request.organization_name,
            slug=slug,
        )

        organization = self.repository.create_organization(
            organization
        )

        organization_settings = build_organization_settings(
            organization.id
        )

        self.repository.create_organization_settings(
            organization_settings
        )

        user = build_user(
            email=request.email,
            password_hash=password_hash,
        )

        user = self.repository.create_user(
            user
        )

        coach_profile = build_coach_profile(
            user_id=user.id,
            first_name=request.owner_first_name,
            last_name=request.owner_last_name,
            phone=request.phone,
        )

        self.repository.create_coach_profile(
            coach_profile
        )

        membership = build_membership(
            organization_id=organization.id,
            user_id=user.id,
            role_id=owner_role.id,
        )

        self.repository.create_membership(
            membership
        )

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

        self.repository.commit()

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

    def login(
        self,
        request: LoginRequest,
    ) -> TokenResponse:

        user = self.repository.get_user_by_email(
            request.email
        )

        if user is None:
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise InactiveUserError(
                "Account is inactive."
            )

        membership = user.organization_memberships[0]
        organization = membership.organization
        role = membership.role
        coach = user.coach_profile

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

        self.repository.update_last_login(
            user
        )

        self.repository.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token_value,
            user=AuthUserResponse(
                id=str(user.id),
                email=user.email,
                first_name=coach.first_name,
                last_name=coach.last_name,
                organization=organization.name,
                role=role.name,
            ),
        )