import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=True,
    )

    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    instructions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    difficulty: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    movement_pattern: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    video_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    thumbnail_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    muscles = relationship(
        "ExerciseMuscle",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )

    equipment = relationship(
        "ExerciseEquipment",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )