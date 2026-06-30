import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ExerciseDifficulty(Base):
    __tablename__ = "exercise_difficulties"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    exercises = relationship(
        "Exercise",
        back_populates="difficulty",
    )

    def __repr__(self):
        return f"<ExerciseDifficulty(name='{self.name}')>"