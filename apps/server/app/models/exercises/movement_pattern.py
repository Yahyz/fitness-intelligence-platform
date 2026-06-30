import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MovementPattern(Base):
    __tablename__ = "movement_patterns"

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

    exercises = relationship(
        "Exercise",
        back_populates="movement_pattern",
    )

    def __repr__(self):
        return f"<MovementPattern(name='{self.name}')>"