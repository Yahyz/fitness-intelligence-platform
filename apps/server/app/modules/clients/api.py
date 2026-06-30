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
    UpdateClientRequest,
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
@router.get(
    "",
    response_model=list[ClientResponse],
)
def list_clients(
    current_user: User = Depends(require_coach),
    db: Session = Depends(get_db),
):
    service = ClientService(db)

    return service.list_clients(current_user)

@router.get(
    "/{client_id}",
    response_model=ClientResponse,
)
def get_client(
    client_id: str,
    current_user: User = Depends(require_coach),
    db: Session = Depends(get_db),
):
    service = ClientService(db)

    return service.get_client(
        client_id,
        current_user,
    )

@router.patch(
    "/{client_id}",
    response_model=ClientResponse,
)
def update_client(
    client_id: str,
    request: UpdateClientRequest,
    current_user: User = Depends(require_coach),
    db: Session = Depends(get_db),
):
    service = ClientService(db)

    return service.update_client(
        client_id,
        request,
        current_user,
    )

@router.delete(
    "/{client_id}",
    status_code=status.HTTP_200_OK,
)
def deactivate_client(
    client_id: str,
    current_user: User = Depends(require_coach),
    db: Session = Depends(get_db),
):

    service = ClientService(db)

    return service.deactivate_client(
        client_id,
        current_user,
    )