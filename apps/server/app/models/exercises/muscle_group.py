import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    exercise_muscles = relationship(
        "ExerciseMuscle",
        back_populates="muscle_group",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<MuscleGroup(name='{self.name}')>"