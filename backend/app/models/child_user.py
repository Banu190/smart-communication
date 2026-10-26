from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import CreatedAtMixin

if TYPE_CHECKING:
    from app.models.child import Child
    from app.models.user import User


class RelationshipType(StrEnum):
    PARENT = "parent"
    SPECIALIST = "specialist"


class ChildUser(CreatedAtMixin, Base):
    __tablename__ = "child_users"

    child_id: Mapped[UUID] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    relationship_type: Mapped[RelationshipType] = mapped_column(
        Enum(
            RelationshipType,
            values_callable=lambda types: [item.value for item in types],
            native_enum=False, create_constraint=True, name="relationship_type",
        )
    )
    child: Mapped[Child] = relationship(back_populates="user_links", lazy="raise")
    user: Mapped[User] = relationship(back_populates="child_links", lazy="raise")
