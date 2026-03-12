from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.case import CaseCreate, CaseRead
from app.services.case_service import CaseService

router = APIRouter(prefix='/cases', tags=['cases'])


@router.post('', response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)) -> CaseRead:
    return CaseService.create_case(db, payload)


@router.get('', response_model=list[CaseRead])
def list_cases(db: Session = Depends(get_db)) -> list[CaseRead]:
    return CaseService.list_cases(db)


@router.get('/{case_id}', response_model=CaseRead)
def get_case(case_id: int, db: Session = Depends(get_db)) -> CaseRead:
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='Case not found')
    return case
