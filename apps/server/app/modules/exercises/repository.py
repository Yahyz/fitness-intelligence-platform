from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models.exercises import (
    Equipment,
    Exercise,
    ExerciseEquipment,
    ExerciseMuscle,
    MuscleGroup,
)


class ExerciseRepository:

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------
    # Exercise
    # -----------------------------

    def create_exercise(
        self,
        exercise: Exercise,
    ) -> Exercise:
        self.db.add(exercise)
        self.db.flush()
        return exercise

    def slug_exists(
        self,
        slug: str,
    ) -> bool:
        statement = select(Exercise).where(
            Exercise.slug == slug
        )
        return self.db.scalar(statement) is not None

    # -----------------------------
    # Lookups
    # -----------------------------

    def get_muscle(
        self,
        muscle_id: UUID,
    ) -> MuscleGroup | None:
        return self.db.get(
            MuscleGroup,
            muscle_id,
        )

    def get_equipment(
        self,
        equipment_id: UUID,
    ) -> Equipment | None:
        return self.db.get(
            Equipment,
            equipment_id,
        )

    # -----------------------------
    # Bridge Tables
    # -----------------------------

    def add_exercise_muscle(
        self,
        mapping: ExerciseMuscle,
    ):
        self.db.add(mapping)

    def add_exercise_equipment(
        self,
        mapping: ExerciseEquipment,
    ):
        self.db.add(mapping)

    # -----------------------------
    # Transactions
    # -----------------------------

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
    
    def list_muscles(
    self,
    ):
        statement = (
            select(MuscleGroup)
            .order_by(MuscleGroup.name)
    )

        return self.db.scalars(statement).all()


    def list_equipment(
        self,
    ):
        statement = (
            select(Equipment)
            .order_by(Equipment.name)
    )

        return self.db.scalars(statement).all()