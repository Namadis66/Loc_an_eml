from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.db.base import Base
from app.db.session import engine
from app.routers import api_cases, api_emails, api_upload, ui

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)

app = FastAPI(title=settings.app_name)
app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.on_event('startup')
def on_startup() -> None:
    settings.storage_root.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)


app.include_router(ui.router)
app.include_router(api_cases.router)
app.include_router(api_upload.router)
app.include_router(api_emails.router)
