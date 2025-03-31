from enum import StrEnum
from pydantic import BaseModel


class DataSourceType(StrEnum):
    WEB = "WEB"
    S3 = "S3"


class KnowledgeBaseModel(BaseModel):
    knowledge_base_id: str
    data_sources: dict[DataSourceType, str]
