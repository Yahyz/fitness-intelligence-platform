from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateExerciseRequest(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str | None = None

    instructions: str | None = None

    difficulty: str

    movement_pattern: str

    video_url: str | None = None

    thumbnail_url: str | None = None

    primary_muscle_ids: list[UUID]

    secondary_muscle_ids: list[UUID] = []

    equipment_ids: list[UUID]


class ExerciseResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    name: str

    description: str | None

    difficulty: str

    movement_pattern: str

    is_active: bool

class LookupResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    name: str