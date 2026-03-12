from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.db.models.case import Case
from app.schemas.case import CaseCreate

logger = logging.getLogger(__name__)


class CaseService:
    @staticmethod
    def create_case(db: Session, payload: CaseCreate) -> Case:
        case = Case(title=payload.title, description=payload.description, status=payload.status)
        db.add(case)
        db.commit()
        db.refresh(case)
        logger.info('Case created', extra={'case_id': case.id})
        return case

    @staticmethod
    def list_cases(db: Session) -> list[Case]:
        return db.query(Case).order_by(Case.created_at.desc()).all()

    @staticmethod
    def get_case(db: Session, case_id: int) -> Case | None:
        return db.query(Case).filter(Case.id == case_id).first()
