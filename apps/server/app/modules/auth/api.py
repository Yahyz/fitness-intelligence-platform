from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InactiveUserError,
    RoleNotFoundError,
)
from app.db.session import get_db
from app.modules.auth.schemas import (
    LoginRequest,
    RegisterOrganizationRequest,
    TokenResponse,
    AuthUserResponse,
)
from app.modules.auth.service import AuthService
from app.core.dependencies import get_current_user
from app.models.identity.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_organization(
    request: RegisterOrganizationRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.register_organization(request)

    except EmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    except RoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    except Exception:
        db.rollback()
        raise

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.login(request)

    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    except InactiveUserError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    except Exception:
        db.rollback()
        raise
@router.get(
    "/me",
    response_model=AuthUserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):

    membership = current_user.organization_memberships[0]

    return AuthUserResponse(
        id=str(current_user.id),
        email=current_user.email,
        first_name=current_user.coach_profile.first_name,
        last_name=current_user.coach_profile.last_name,
        organization=membership.organization.name,
        role=membership.role.name,
    )