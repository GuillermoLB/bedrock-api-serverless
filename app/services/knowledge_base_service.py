from datetime import datetime
from enum import Enum, StrEnum
import os
from app.schemas.knowledge_base_schemas import DataSourceType, KnowledgeBaseModel
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from botocore.exceptions import NoCredentialsError, ClientError
import io
import boto3
import json
import logging
import base64


def ingest_data_source(bedrock: any, knowledge_base: KnowledgeBaseModel, source: DataSourceType) -> None:
    start_job_response = bedrock.start_ingestion_job(
        knowledgeBaseId= knowledge_base.knowledge_base_id,
        dataSourceId= knowledge_base.data_sources[source]
    )