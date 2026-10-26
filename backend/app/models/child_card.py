from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, false, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import CreatedAtMixin

if TYPE_CHECKING:
    from app.models.card import Card
    from app.models.child import Child


class ChildCard(CreatedAtMixin, Base):
    __tablename__ = "child_cards"

    # The composite primary key also guarantees uniqueness of the pair.
    child_id: Mapped[UUID] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), primary_key=True
    )
    card_id: Mapped[UUID] = mapped_column(
        ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0")
    )
    is_favorite: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false()
    )
    child: Mapped[Child] = relationship(back_populates="card_links", lazy="raise")
    card: Mapped[Card] = relationship(back_populates="child_links", lazy="raise")
