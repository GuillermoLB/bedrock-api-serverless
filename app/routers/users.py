import logging
from fastapi import APIRouter
from app.core.config import Settings


settings = Settings()
router = APIRouter()
logger = logging.getLogger(__name__)
