from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.db.models.attachment import Attachment
from app.db.models.case import Case
from app.db.models.email_message import EmailMessage
from app.db.models.uploaded_file import UploadedFile
from app.services.eml_parser import parse_eml_file

logger = logging.getLogger(__name__)


class UploadService:
    @staticmethod
    def upload_eml(db: Session, case: Case, file: UploadFile) -> UploadedFile:
        case_dir = settings.storage_root / 'cases' / str(case.id)
        source_dir = case_dir / 'source_eml'
        attachment_dir = case_dir / 'attachments'
        source_dir.mkdir(parents=True, exist_ok=True)

        original_name = file.filename or 'email.eml'
        target_path = source_dir / original_name
        raw = file.file.read()
        target_path.write_bytes(raw)

        uploaded = UploadedFile(
            case_id=case.id,
            original_name=original_name,
            storage_path=str(target_path),
            size_bytes=len(raw),
            sha256=hashlib.sha256(raw).hexdigest(),
            parse_status='processing',
        )
        db.add(uploaded)
        db.commit()
        db.refresh(uploaded)

        try:
            parsed = parse_eml_file(target_path, attachment_dir / f'email_{uploaded.id}')
            email = EmailMessage(
                case_id=case.id,
                uploaded_file_id=uploaded.id,
                message_id=parsed.message_id,
                subject_raw=parsed.subject_raw,
                subject_normalized=parsed.subject_normalized,
                date_raw=parsed.date_raw,
                sent_at=parsed.sent_at,
                from_name=parsed.from_name,
                from_email=parsed.from_email,
                to_json=parsed.to_json,
                cc_json=parsed.cc_json,
                body_text_raw=parsed.body_text_raw,
                body_html_raw=parsed.body_html_raw,
                body_text_clean=parsed.body_text_clean,
            )
            db.add(email)
            db.flush()

            for item in parsed.attachments:
                db.add(
                    Attachment(
                        email_id=email.id,
                        filename=item.filename,
                        mime_type=item.mime_type,
                        size_bytes=item.size_bytes,
                        sha256=item.sha256,
                        storage_path=item.storage_path,
                        is_inline=item.is_inline,
                    )
                )

            uploaded.parse_status = 'parsed'
            uploaded.parse_error = None
            db.commit()
            logger.info('Uploaded and parsed eml', extra={'case_id': case.id, 'uploaded_file_id': uploaded.id})
        except Exception as exc:
            db.rollback()
            uploaded = db.get(UploadedFile, uploaded.id)
            if uploaded:
                uploaded.parse_status = 'failed'
                uploaded.parse_error = str(exc)
                db.commit()
            logger.exception('Failed to parse eml', extra={'case_id': case.id, 'uploaded_file_id': uploaded.id if uploaded else None})

        return db.get(UploadedFile, uploaded.id)
