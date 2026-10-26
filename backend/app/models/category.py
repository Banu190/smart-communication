from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Integer, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import CreatedAtMixin

if TYPE_CHECKING:
    from app.models.card import Card


class Category(CreatedAtMixin, Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("slug", name="uq_categories_slug"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name_kk: Mapped[str] = mapped_column(String(255))
    name_ru: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0")
    )

    cards: Mapped[list[Card]] = relationship(
        back_populates="category", lazy="raise", passive_deletes="all"
    )
