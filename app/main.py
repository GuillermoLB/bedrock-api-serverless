import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request

from app.core.log_config import LogConfig
from app.dependencies import get_settings
from app.routers import users


logging.config.dictConfig(LogConfig().model_dump())

logger = logging.getLogger(__name__)

settings = get_settings()


app = FastAPI(
    title="Roams AI API",
    description="""
""",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "User management and authentication",
        },
    ]
)


# Include API routes
app.include_router(users.router, tags=["Users"])


# Middleware to log requests and responses
@app.middleware("http")
async def log_request_response(request: Request, call_next):
    request_id = str(uuid4())
    start_time = time.time()

    # Log request metadata
    path = request.url.path + \
        ("?" + request.url.query if request.url.query else "")
    logger.info(f"Request {request_id}: {request.method} {path}")

    # Process request
    response = await call_next(request)

    # Log response metadata
    process_time = round((time.time() - start_time) * 1000)
    logger.info(
        f"Response {request_id}: Status={
            response.status_code} Duration={process_time}ms "
        f"Method={request.method} Path={path}"
    )

    return response


@app.get("/")
def health_check():
    return {"status": "OK"}
