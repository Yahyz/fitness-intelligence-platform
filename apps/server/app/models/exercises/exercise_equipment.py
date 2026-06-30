import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ExerciseEquipment(Base):
    __tablename__ = "exercise_equipment"

    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
    )

    equipment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("equipment.id", ondelete="CASCADE"),
        primary_key=True,
    )

    exercise = relationship(
        "Exercise",
        back_populates="equipment",
    )

    equipment = relationship(
        "Equipment",
        back_populates="exercise_equipment",
    )