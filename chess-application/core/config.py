import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql+asyncpg://root:password@localhost:5432/postgres")
    DEBUG: bool = False

settings = Settings()