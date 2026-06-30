from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    require_coach,
)
from app.db.session import get_db
from app.models.identity.user import User
from app.modules.exercises.schemas import (
    CreateExerciseRequest,
    ExerciseResponse,
    LookupResponse,
)
from app.modules.exercises.service import ExerciseService

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"],
)


@router.post(
    "",
    response_model=ExerciseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_exercise(
    request: CreateExerciseRequest,
    current_user: User = Depends(require_coach),
    db: Session = Depends(get_db),
):

    service = ExerciseService(db)

    return service.create_exercise(
        request,
        current_user,
    )

@router.get(
    "/muscles",
    response_model=list[LookupResponse],
)
def list_muscles(
    db: Session = Depends(get_db),
):

    service = ExerciseService(db)

    return service.list_muscles()
@router.get(
    "/equipment",
    response_model=list[LookupResponse],
)
def list_equipment(
    db: Session = Depends(get_db),
):

    service = ExerciseService(db)

    return service.list_equipment()