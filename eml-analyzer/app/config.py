from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = Field(default='EML Analyzer', alias='APP_NAME')
    app_env: str = Field(default='dev', alias='APP_ENV')
    database_url: str = Field(default='sqlite:///./storage/app.db', alias='DATABASE_URL')
    storage_root: Path = Field(default=Path('./storage'), alias='STORAGE_ROOT')
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')


settings = Settings()
