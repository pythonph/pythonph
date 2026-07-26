import re
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]

LOCAL_POSTGRES_URL = "postgres://postgres:postgres@localhost"


class Settings(BaseSettings):
    APP_ENV: str = Field(default="development")
    BASE_URL: str = Field(default="http://localhost:8000")
    SECRET_KEY: str = Field(default="django-insecure-pythonph-dev-key-change-in-production")
    DEBUG: bool = Field(default=True)
    ALLOWED_HOSTS: list[str] = Field(default=[])
    DATABASE_URL: str = Field(default=LOCAL_POSTGRES_URL)
    TRUSTED_ORIGINS: list[str] = Field(default=[])
    SENTRY_DSN: str = Field(default="")

    # Slack integration
    SLACK_ORG: str = Field(default="")
    SLACK_API_TOKEN: str = Field(default="")
    SLACK_BOARD_CHANNEL: str = Field(default="")
    SLACK_JOBS_CHANNEL: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    def get_allowed_hosts(self):
        return self.ALLOWED_HOSTS or [
            "localhost",
            "127.0.0.1",
            "python.ph",
            "www.python.ph",
        ]

    def get_trusted_origins(self):
        return self.TRUSTED_ORIGINS or [
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "https://python.ph",
            "https://www.python.ph",
        ]

    def get_db_config(self):
        regex = r"postgresql://(.*?):(.*?)@(.*?)/(.*)"
        user, pwd, host, name = re.match(regex, self.DATABASE_URL).groups()
        return {"NAME": name, "HOST": host, "USER": user, "PASSWORD": pwd, "PORT": 5432}


settings = Settings()
