from app.builders import build_exercise
from app.modules.exercises.repository import ExerciseRepository
from app.modules.exercises.schemas import (
    CreateExerciseRequest,
    ExerciseResponse,
    LookupResponse,
)
from app.models.exercises import (
    ExerciseEquipment,
    ExerciseMuscle,
    
)
from app.shared.slug import generate_unique_slug


class ExerciseService:

    def __init__(self, db):
        self.repository = ExerciseRepository(db)

    def create_exercise(
        self,
        request: CreateExerciseRequest,
        current_user,
    ) -> ExerciseResponse:

        organization = (
            current_user.organization_memberships[0]
            .organization
        )

        slug = generate_unique_slug(
            request.name,
            self.repository,
        )

        exercise = build_exercise(
            organization_id=organization.id,
            created_by=current_user.id,
            name=request.name,
            slug=slug,
            description=request.description,
            instructions=request.instructions,
            difficulty=request.difficulty,
            movement_pattern=request.movement_pattern,
            video_url=request.video_url,
            thumbnail_url=request.thumbnail_url,
        )

        exercise = self.repository.create_exercise(
            exercise
        )

        # Primary muscles

        for muscle_id in request.primary_muscle_ids:

            if self.repository.get_muscle(muscle_id) is None:
                raise ValueError(
                    "Invalid muscle group."
                )

            self.repository.add_exercise_muscle(
                ExerciseMuscle(
                    exercise_id=exercise.id,
                    muscle_group_id=muscle_id,
                    is_primary=True,
                )
            )

        # Secondary muscles

        for muscle_id in request.secondary_muscle_ids:

            if self.repository.get_muscle(muscle_id) is None:
                raise ValueError(
                    "Invalid muscle group."
                )

            self.repository.add_exercise_muscle(
                ExerciseMuscle(
                    exercise_id=exercise.id,
                    muscle_group_id=muscle_id,
                    is_primary=False,
                )
            )

        # Equipment

        for equipment_id in request.equipment_ids:

            if self.repository.get_equipment(
                equipment_id
            ) is None:
                raise ValueError(
                    "Invalid equipment."
                )

            self.repository.add_exercise_equipment(
                ExerciseEquipment(
                    exercise_id=exercise.id,
                    equipment_id=equipment_id,
                )
            )

        self.repository.commit()

        return ExerciseResponse(
            id=exercise.id,
            name=exercise.name,
            description=exercise.description,
            difficulty=exercise.difficulty,
            movement_pattern=exercise.movement_pattern,
            is_active=exercise.is_active,
        )
    def list_muscles(
    self,
    ):

        muscles = self.repository.list_muscles()

        return [
         LookupResponse.model_validate(
            muscle
        )
        for muscle in muscles
    ]


    def list_equipment(
        self,
    ):

        equipment = self.repository.list_equipment()

        return [
            LookupResponse.model_validate(
            item
            )
            for item in equipment
        ]