from __future__ import annotations

import re


def normalize_subject(subject: str | None) -> str | None:
    if not subject:
        return None
    normalized = re.sub(r'^(re|fw|fwd)\s*:\s*', '', subject, flags=re.IGNORECASE)
    return normalized.strip() or None


def clean_text(text: str | None) -> str | None:
    if not text:
        return None
    text = text.replace('\r\n', '\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() or None
