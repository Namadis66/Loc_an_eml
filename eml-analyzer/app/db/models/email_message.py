from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EmailMessage(Base):
    __tablename__ = 'email_messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey('cases.id', ondelete='CASCADE'), index=True)
    uploaded_file_id: Mapped[int] = mapped_column(ForeignKey('uploaded_files.id', ondelete='CASCADE'), unique=True)

    message_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subject_raw: Mapped[str | None] = mapped_column(String(998), nullable=True)
    subject_normalized: Mapped[str | None] = mapped_column(String(998), nullable=True, index=True)

    date_raw: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    from_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    from_email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    to_json: Mapped[str | None] = mapped_column(Text(), nullable=True)
    cc_json: Mapped[str | None] = mapped_column(Text(), nullable=True)

    body_text_raw: Mapped[str | None] = mapped_column(Text(), nullable=True)
    body_html_raw: Mapped[str | None] = mapped_column(Text(), nullable=True)
    body_text_clean: Mapped[str | None] = mapped_column(Text(), nullable=True)

    thread_id: Mapped[int | None] = mapped_column(ForeignKey('threads.id', ondelete='SET NULL'), nullable=True)

    case = relationship('Case', back_populates='emails')
    uploaded_file = relationship('UploadedFile', back_populates='email')
    attachments = relationship('Attachment', back_populates='email', cascade='all, delete-orphan')
    thread = relationship('Thread', back_populates='emails')
    events = relationship('Event', back_populates='email', cascade='all, delete-orphan')
