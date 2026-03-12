# EML Analyzer (MVP)

Локальное веб-приложение для загрузки и анализа `.eml` файлов с сохранением в SQLite.

## Стек
- Python 3.11+
- FastAPI + Jinja2 + HTMX
- SQLAlchemy ORM + SQLite

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --app-dir .
```

Открыть: http://127.0.0.1:8000

## Что реализовано
- Создание и список дел (`Case`)
- Загрузка `.eml` в дело
- Сохранение файлов на диск (`storage/cases/<case_id>/source_eml`)
- Парсинг email (headers, text/plain, text/html, attachments)
- Сохранение в SQLite (`Case`, `UploadedFile`, `EmailMessage`, `Attachment` + базовые сущности для расширения)
- Базовый UI на Jinja2

## API
- `POST /cases`
- `GET /cases`
- `GET /cases/{case_id}`
- `POST /cases/{case_id}/upload`
- `GET /cases/{case_id}/emails`
- `GET /cases/{case_id}/emails/{email_id}`

## Архитектура
Слоистый подход:
- `routers/` — только HTTP endpoints
- `services/` — бизнес-логика
- `db/models/` — ORM модели
- `schemas/` — API схемы
