from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.case_service import CaseService
from app.services.upload_service import UploadService

router = APIRouter(tags=['upload'])


@router.post('/cases/{case_id}/upload')
def upload_eml(case_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)) -> dict[str, str | int | None]:
    if not file.filename or not file.filename.lower().endswith('.eml'):
        raise HTTPException(status_code=400, detail='Only .eml files are supported')

    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='Case not found')

    uploaded = UploadService.upload_eml(db, case, file)
    return {
        'uploaded_file_id': uploaded.id,
        'parse_status': uploaded.parse_status,
        'parse_error': uploaded.parse_error,
    }
