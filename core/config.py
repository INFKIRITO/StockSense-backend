from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Literal

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "Scoutsense AI"
    env: str = "development"

    ai_matching_mode: Literal["keyword", "semantic"] = "keyword"


    class Config:
        env_file = ".env"
        case_sensitive = False  # 👈 important on Windows


settings = Settings()