from app.models.identity.organization import Organization
from app.models.identity.organization_settings import OrganizationSettings


def build_organization(
    name: str,
    slug: str,
) -> Organization:
    return Organization(
        name=name,
        slug=slug,
    )


def build_organization_settings(
    organization_id,
) -> OrganizationSettings:
    return OrganizationSettings(
        organization_id=organization_id,
    )