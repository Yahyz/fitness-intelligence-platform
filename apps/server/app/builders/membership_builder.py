from app.models.identity.organization_member import OrganizationMember


def build_membership(
    organization_id,
    user_id,
    role_id: int,
) -> OrganizationMember:
    return OrganizationMember(
        organization_id=organization_id,
        user_id=user_id,
        role_id=role_id,
    )