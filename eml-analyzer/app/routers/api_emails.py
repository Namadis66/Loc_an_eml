from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.email_message import EmailMessage
from app.db.session import get_db
from app.schemas.email import EmailRead
from app.services.case_service import CaseService

router = APIRouter(prefix='/cases/{case_id}/emails', tags=['emails'])


@router.get('', response_model=list[EmailRead])
def list_case_emails(case_id: int, db: Session = Depends(get_db)) -> list[EmailRead]:
    if not CaseService.get_case(db, case_id):
        raise HTTPException(status_code=404, detail='Case not found')
    return db.query(EmailMessage).filter(EmailMessage.case_id == case_id).order_by(EmailMessage.id.desc()).all()


@router.get('/{email_id}', response_model=EmailRead)
def get_email(case_id: int, email_id: int, db: Session = Depends(get_db)) -> EmailRead:
    email = db.query(EmailMessage).filter(EmailMessage.case_id == case_id, EmailMessage.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail='Email not found')
    return email
