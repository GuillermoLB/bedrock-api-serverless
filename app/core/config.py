import os
from typing import Any, ClassVar, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_ssm_settings import SsmBaseSettings


class Settings(SsmBaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')

    # AWS credentials
    AWS_ACCESS_KEY_ID: str = "test-access-key"
    AWS_SECRET_ACCESS_KEY: str = "test-secret-key"
    AWS_DEFAULT_REGION: str = "us-east-1"

    # PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres_tests"

    # AWS
    AWS_REGION: str = "us-east-1"
    AGENT_ID: str = "test-agent-id"
    AGENT_ALIAS_ID: str = "test-alias-id"
    KNOWLEDGE_BASE_ID: str = "test-knowledge-base-id"
    ENCRIPTION_KEY_ARN: str = "test-key-arn"
    MEMORY_TYPE: str = "DEFAULT"
    MEMORY_MAX_ITEMS: int = 10
    MESSAGES_MAX_RESULTS: int = 20
    LOG_GROUP_NAME: str = "test-log-group"
    LOG_STREAM_NAME: str = "test-log-stream"
    RERANKING_MODEL: str = "test:reranking:model"

    # JWT
    SECRET_KEY: str = "testsecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TOKEN_TYPE: str = "Bearer"

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


settings = Settings()
