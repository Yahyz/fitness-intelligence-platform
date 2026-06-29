from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.models.identity.user import User


def _require_role(*allowed_roles: str):
    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:

        membership = current_user.organization_memberships[0]

        role_name = membership.role.name

        if role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action.",
            )

        return current_user

    return dependency


require_owner = _require_role("Owner")

require_admin = _require_role(
    "Owner",
    "Admin",
)

require_coach = _require_role(
    "Owner",
    "Admin",
    "Coach",
)

require_client = _require_role(
    "Client",
)