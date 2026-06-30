from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.models.exercises import (
    Equipment,
    MuscleGroup,
)

from app.seeds.equipment import EQUIPMENT
from app.seeds.muscle_groups import MUSCLE_GROUPS


def seed_muscle_groups(db: Session):

    for name in MUSCLE_GROUPS:

        exists = (
            db.query(MuscleGroup)
            .filter(MuscleGroup.name == name)
            .first()
        )

        if not exists:
            db.add(
                MuscleGroup(name=name)
            )


def seed_equipment(db: Session):

    for name in EQUIPMENT:

        exists = (
            db.query(Equipment)
            .filter(Equipment.name == name)
            .first()
        )

        if not exists:
            db.add(
                Equipment(name=name)
            )


def main():

    db = SessionLocal()

    try:

        seed_muscle_groups(db)

        seed_equipment(db)

        db.commit()

        print("✅ Exercise library seeded.")

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()