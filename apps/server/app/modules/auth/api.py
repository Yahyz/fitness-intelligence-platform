from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import (
    EmailAlreadyExistsError,
    RoleNotFoundError,
)
from app.db.session import get_db
from app.modules.auth.schemas import (
    RegisterOrganizationRequest,
    TokenResponse,
)
from app.modules.auth.service import AuthService

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