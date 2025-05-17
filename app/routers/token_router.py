import logging
from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.token_schemas import TokenCreate
from app.services.user_service import authenticate_user, create_access_token
from app.core.config import settings

tokens_router = APIRouter(
    tags=["tokens"],
    prefix="/tokens",
)

logger = logging.getLogger(__name__)

# Change tokenUrl to match our endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="tokens/token")

# Add token generation endpoint


@tokens_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_create = TokenCreate(
        username=user.username,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    token = create_access_token(
        token_create
    )
    return token


@tokens_router.get("")
async def get_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
