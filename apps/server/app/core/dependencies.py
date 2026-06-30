from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.identity.user import User
from app.modules.auth.repository import AuthRepository

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:

    token = credentials.credentials

    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    repository = AuthRepository(db)

    user = repository.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive account.",
        )

    return user

def require_coach(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allows authenticated coaches/owners to access coach endpoints.
    """

    if not current_user.organization_memberships:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No organization membership.",
        )

    membership = current_user.organization_memberships[0]

    role = membership.role

    if role.name not in (
        "Owner",
        "Coach",
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Coach access required.",
        )

    return current_user

def require_owner(
    current_user: User = Depends(get_current_user),
) -> User:

    if not current_user.organization_memberships:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No organization membership.",
        )

    membership = current_user.organization_memberships[0]

    if membership.role.name != "Owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner access required.",
        )

    return current_user