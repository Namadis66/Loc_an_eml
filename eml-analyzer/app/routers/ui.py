from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.models.email_message import EmailMessage
from app.db.session import get_db
from app.services.case_service import CaseService

router = APIRouter(tags=['ui'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    cases = CaseService.list_cases(db)
    return templates.TemplateResponse('index.html', {'request': request, 'cases': cases})


@router.get('/cases/{case_id}', response_class=HTMLResponse)
def case_detail(case_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='Case not found')
    return templates.TemplateResponse('case_detail.html', {'request': request, 'case': case})


@router.get('/cases/{case_id}/emails/view', response_class=HTMLResponse)
def emails_list(case_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='Case not found')
    emails = db.query(EmailMessage).filter(EmailMessage.case_id == case_id).order_by(EmailMessage.id.desc()).all()
    return templates.TemplateResponse('emails_list.html', {'request': request, 'case': case, 'emails': emails})


@router.get('/cases/{case_id}/emails/{email_id}/view', response_class=HTMLResponse)
def email_detail(case_id: int, email_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    email = db.query(EmailMessage).filter(EmailMessage.case_id == case_id, EmailMessage.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail='Email not found')
    return templates.TemplateResponse('email_detail.html', {'request': request, 'email': email})
