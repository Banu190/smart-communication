from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Enum, Index, String, Text, func, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin

if TYPE_CHECKING:
    from app.models.child_user import ChildUser


class UserRole(StrEnum):
    PARENT = "parent"
    SPECIALIST = "specialist"
    ADMIN = "admin"


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(320))
    # Only a hash produced by the future authentication service belongs here.
    password_hash: Mapped[str] = mapped_column(Text)
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            values_callable=lambda roles: [role.value for role in roles],
            native_enum=False, create_constraint=True, name="user_role",
        )
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true()
    )

    child_links: Mapped[list[ChildUser]] = relationship(
        back_populates="user", lazy="raise", cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("uq_users_email_lower", func.lower(email), unique=True),
    )
