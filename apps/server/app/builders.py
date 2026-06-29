from datetime import datetime, timedelta
from uuid import UUID

from app.core.config import settings
from app.models.identity.coach_profile import CoachProfile
from app.models.identity.organization import Organization
from app.models.identity.organization_member import OrganizationMember
from app.models.identity.organization_settings import OrganizationSettings
from app.models.identity.refresh_token import RefreshToken
from app.models.identity.user import User


def build_organization(
    name: str,
    slug: str,
) -> Organization:
    return Organization(
        name=name,
        slug=slug,
    )


def build_user(
    email: str,
    password_hash: str,
) -> User:
    return User(
        email=email.lower(),
        password_hash=password_hash,
        is_active=True,
        is_verified=False,
    )


def build_coach_profile(
    user_id: UUID,
    first_name: str,
    last_name: str,
    phone: str | None = None,
) -> CoachProfile:
    return CoachProfile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )


def build_organization_settings(
    organization_id: UUID,
) -> OrganizationSettings:
    return OrganizationSettings(
        organization_id=organization_id,
    )


def build_membership(
    organization_id: UUID,
    user_id: UUID,
    role_id: int,
) -> OrganizationMember:
    return OrganizationMember(
        organization_id=organization_id,
        user_id=user_id,
        role_id=role_id,
    )


def build_refresh_token(
    user_id: UUID,
    token: str,
) -> RefreshToken:
    return RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=datetime.utcnow()
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False,
    )