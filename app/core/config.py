from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI: str = "postgresql://user:password@localhost:5432/dbname"

    # Logging
    LOG_LEVEL: str = "INFO"
    DISABLE_LOGGERS: bool = False

    # PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"

    def get_connection_str(self):
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"


settings = Settings()
