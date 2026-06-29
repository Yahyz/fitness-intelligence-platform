from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.exceptions import (
    ClientAlreadyExistsError,
    ClientRoleNotFoundError,
)
from app.core.permissions import require_coach
from app.models.identity.user import User
from app.modules.clients.schemas import (
    ClientResponse,
    CreateClientRequest,
)
from app.modules.clients.service import ClientService

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


@router.get("/health")
def health_check(
    current_user: User = Depends(require_coach),
):
    return {
        "message": "Clients module is working."
    }


@router.post(
    "",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_client(
    request: CreateClientRequest,
    current_user: User = Depends(require_coach),
    db: Session = Depends(get_db),
):
    service = ClientService(db)

    try:
        return service.create_client(
            request=request,
            current_user=current_user,
        )

    except ClientAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    except ClientRoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    except Exception:
        db.rollback()
        raise