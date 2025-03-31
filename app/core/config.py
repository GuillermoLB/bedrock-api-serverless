from app.schemas.knowledge_base_schemas import DataSourceType, KnowledgeBaseModel
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Logging
    LOG_LEVEL: str = "INFO"
    DISABLE_LOGGERS: bool = False

    # PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    KNOWLEDGE_BASE: KnowledgeBaseModel = KnowledgeBaseModel(
        knowledge_base_id = "kb12345",
        data_sources = {
            DataSourceType.WEB: "web12345",
            DataSourceType.S3: "s312345"
        }
    )
    AGENT: AgentModel = AgentModel(
        agent_id = "agent12345",
        agent_alias_id = "alias12345"
    )

    def get_connection_str(self):
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"



settings = Settings()
