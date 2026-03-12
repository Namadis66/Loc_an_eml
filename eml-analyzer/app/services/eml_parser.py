from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from email import policy
from email.header import decode_header, make_header
from email.parser import BytesParser
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path

import html2text
from bs4 import BeautifulSoup

from app.services.text_cleaner import clean_text, normalize_subject


@dataclass
class ParsedAttachment:
    filename: str | None
    mime_type: str | None
    size_bytes: int
    sha256: str
    storage_path: str
    is_inline: bool


@dataclass
class ParsedEmail:
    message_id: str | None
    subject_raw: str | None
    subject_normalized: str | None
    date_raw: str | None
    sent_at: datetime | None
    from_name: str | None
    from_email: str | None
    to_json: str
    cc_json: str
    body_text_raw: str | None
    body_html_raw: str | None
    body_text_clean: str | None
    attachments: list[ParsedAttachment] = field(default_factory=list)


def _decode_header_value(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def _addresses_to_json(value: str | None) -> str:
    addresses = getaddresses([value or ''])
    data = [{'name': _decode_header_value(name), 'email': email} for name, email in addresses if email]
    return json.dumps(data, ensure_ascii=False)


def parse_eml_file(file_path: Path, attachments_dir: Path) -> ParsedEmail:
    msg = BytesParser(policy=policy.default).parsebytes(file_path.read_bytes())

    body_text_raw: str | None = None
    body_html_raw: str | None = None
    attachments: list[ParsedAttachment] = []

    attachments_dir.mkdir(parents=True, exist_ok=True)

    for part in msg.walk():
        content_disposition = part.get_content_disposition()
        content_type = part.get_content_type()

        if content_disposition == 'attachment' or (part.get_filename() and content_type != 'text/plain'):
            raw = part.get_payload(decode=True) or b''
            filename = _decode_header_value(part.get_filename()) or 'attachment.bin'
            safe_name = filename.replace('/', '_').replace('\\', '_')
            target = attachments_dir / safe_name
            target.write_bytes(raw)
            attachments.append(
                ParsedAttachment(
                    filename=filename,
                    mime_type=content_type,
                    size_bytes=len(raw),
                    sha256=hashlib.sha256(raw).hexdigest(),
                    storage_path=str(target),
                    is_inline=content_disposition == 'inline',
                )
            )
            continue

        if content_type == 'text/plain' and body_text_raw is None:
            body_text_raw = part.get_content()
        elif content_type == 'text/html' and body_html_raw is None:
            body_html_raw = part.get_content()

    text_from_html: str | None = None
    if body_html_raw:
        soup = BeautifulSoup(body_html_raw, 'html.parser')
        text_from_html = html2text.html2text(str(soup))

    combined_text = clean_text(body_text_raw or text_from_html)

    date_raw = _decode_header_value(msg.get('Date'))
    sent_at = None
    if date_raw:
        try:
            sent_at = parsedate_to_datetime(date_raw)
        except (TypeError, ValueError):
            sent_at = None

    from_name, from_email = ('', '')
    parsed_from = getaddresses([msg.get('From', '')])
    if parsed_from:
        from_name, from_email = parsed_from[0]

    subject_raw = _decode_header_value(msg.get('Subject'))

    return ParsedEmail(
        message_id=_decode_header_value(msg.get('Message-ID')),
        subject_raw=subject_raw,
        subject_normalized=normalize_subject(subject_raw),
        date_raw=date_raw,
        sent_at=sent_at,
        from_name=_decode_header_value(from_name),
        from_email=from_email or None,
        to_json=_addresses_to_json(msg.get('To')),
        cc_json=_addresses_to_json(msg.get('Cc')),
        body_text_raw=body_text_raw,
        body_html_raw=body_html_raw,
        body_text_clean=combined_text,
        attachments=attachments,
    )
