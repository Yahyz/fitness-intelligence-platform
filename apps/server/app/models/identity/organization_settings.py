import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OrganizationSettings(Base):
    __tablename__ = "organization_settings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        unique=True,
    )

    measurement_system: Mapped[str] = mapped_column(
        String(10),
        default="metric",
    )

    week_start: Mapped[str] = mapped_column(
        String(20),
        default="monday",
    )

    notifications_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    organization = relationship("Organization")