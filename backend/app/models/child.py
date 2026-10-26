from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin

if TYPE_CHECKING:
    from app.models.child_card import ChildCard
    from app.models.child_user import ChildUser


class Child(TimestampMixin, Base):
    __tablename__ = "children"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    full_name: Mapped[str] = mapped_column(String(255))
    birth_date: Mapped[date | None] = mapped_column(Date)
    # General communication notes only; do not store diagnoses here.
    notes: Mapped[str | None] = mapped_column(Text)

    user_links: Mapped[list[ChildUser]] = relationship(
        back_populates="child", lazy="raise", cascade="all, delete-orphan",
        passive_deletes=True,
    )
    card_links: Mapped[list[ChildCard]] = relationship(
        back_populates="child", lazy="raise", cascade="all, delete-orphan",
        passive_deletes=True,
    )
