from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Logging
    LOG_LEVEL: str = "INFO"
    DISABLE_LOGGERS: bool = False


class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"
