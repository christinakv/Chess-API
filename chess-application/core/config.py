from typing import Optional
import os
from pydantic import Field, Secret
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = Field(
        default=os.environ.get("DATABASE_URL"), env="DATABASE_URL"
    )
    DEBUG: bool = Field(default=False, env="DEBUG")
    run: Optional[dict] = Field(default=None)

class DevelopmentSettings(Settings):
    DEBUG: bool = True
    run = Settings.run.copy(update={"host": "0.0.0.0", "port": 8000})

settings = Settings()

if os.environ.get("ENVIRONMENT") == "development":
    settings = DevelopmentSettings()