from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, String, Text, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.child_card import ChildCard


class Card(TimestampMixin, Base):
    __tablename__ = "cards"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), index=True
    )
    title_kk: Mapped[str] = mapped_column(String(255))
    title_ru: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str] = mapped_column(Text)
    audio_url_kk: Mapped[str | None] = mapped_column(Text)
    audio_url_ru: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true()
    )

    category: Mapped[Category] = relationship(back_populates="cards", lazy="raise")
    child_links: Mapped[list[ChildCard]] = relationship(
        back_populates="card", lazy="raise", cascade="all, delete-orphan",
        passive_deletes=True,
    )
