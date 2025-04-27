import os
from typing import Any, ClassVar, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_ssm_settings import SsmBaseSettings


class Settings(SsmBaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    # AWS
    AWS_REGION: str
    AGENT_ID: str
    AGENT_ALIAS_ID: str
    KNOWLEDGE_BASE_ID: str
    ENCRIPTION_KEY_ARN: str
    MEMORY_TYPE:str
    MEMORY_MAX_ITEMS: int
    MESSAGES_MAX_RESULTS: int
    LOG_GROUP_NAME: str
    LOG_STREAM_NAME: str
    RERANKING_MODEL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"
    DISABLE_LOGGERS: bool = False

    def get_reranking_config(self) -> Dict[str, Any]:
        """Get reranking configuration"""
        return {
            'bedrockRerankingConfiguration': {
                'metadataConfiguration': {
                    'selectionMode': 'SELECTIVE',
                    'selectiveModeConfiguration': {
                        'fieldsToInclude': [
                            {'fieldName': 'es_interno'},
                            {'fieldName': 'compania'},
                        ],
                    }
                },
                'modelConfiguration': {
                    'modelArn': self.RERANKING_MODEL,
                },
                'numberOfRerankedResults': 4,
            },
            'type': 'BEDROCK_RERANKING_MODEL',
        }
    
    def get_session_state(self) -> Dict[str, Any]:
        """Get session state configuration"""
        return {
            'knowledgeBaseConfigurations': [
                {
                    'knowledgeBaseId': self.KNOWLEDGE_BASE_ID,
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': 18,
                            'overrideSearchType': 'HYBRID',
                            'rerankingConfiguration': self.get_reranking_config(),
                        }
                    },
                },
            ]
        }
    
    def get_connection_str(self):
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings(_ssm_prefix="/zappapi/")

print(settings.model_dump())

