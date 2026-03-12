from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey('cases.id', ondelete='CASCADE'), index=True)
    email_id: Mapped[int | None] = mapped_column(ForeignKey('email_messages.id', ondelete='SET NULL'), nullable=True)
    event_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text(), nullable=True)

    case = relationship('Case', back_populates='events')
    email = relationship('EmailMessage', back_populates='events')
