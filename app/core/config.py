from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI: str = "postgresql://user:password@localhost:5432/dbname"

    # Logging
    LOG_LEVEL: str = "INFO"
    DISABLE_LOGGERS: bool = False


class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"


settings = Settings()
