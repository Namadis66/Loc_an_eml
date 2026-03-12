from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttachmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str | None
    mime_type: str | None
    size_bytes: int
    sha256: str | None
    is_inline: bool


class EmailRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    case_id: int
    subject_raw: str | None
    subject_normalized: str | None
    message_id: str | None
    sent_at: datetime | None
    from_name: str | None
    from_email: str | None
    body_text_clean: str | None
