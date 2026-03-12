from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Thread(Base):
    __tablename__ = 'threads'

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey('cases.id', ondelete='CASCADE'), index=True)
    subject_normalized: Mapped[str | None] = mapped_column(String(998), nullable=True, index=True)
    root_email_id: Mapped[int | None] = mapped_column(ForeignKey('email_messages.id', ondelete='SET NULL'), nullable=True)

    case = relationship('Case', back_populates='threads')
    emails = relationship('EmailMessage', back_populates='thread', foreign_keys='EmailMessage.thread_id')
