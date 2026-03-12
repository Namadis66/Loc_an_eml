from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Case(Base):
    __tablename__ = 'cases'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default='new', nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    uploaded_files = relationship('UploadedFile', back_populates='case', cascade='all, delete-orphan')
    emails = relationship('EmailMessage', back_populates='case', cascade='all, delete-orphan')
    threads = relationship('Thread', back_populates='case', cascade='all, delete-orphan')
    events = relationship('Event', back_populates='case', cascade='all, delete-orphan')
    notes = relationship('AnalysisNote', back_populates='case', cascade='all, delete-orphan')
