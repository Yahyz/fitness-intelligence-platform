import uuid

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ExerciseMuscle(Base):
    __tablename__ = "exercise_muscles"

    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
    )

    muscle_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("muscle_groups.id", ondelete="CASCADE"),
        primary_key=True,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    exercise = relationship(
        "Exercise",
        back_populates="muscles",
    )

    muscle_group = relationship(
        "MuscleGroup",
        back_populates="exercise_muscles",
    )