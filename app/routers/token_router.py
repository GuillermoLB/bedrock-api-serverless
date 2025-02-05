import logging
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.dependencies import SettingsDep
from app.repos import user_repo
from app.schemas.user_schemas import UserRead, UserCreate
from app.dependencies import SessionDep

tokens_router = APIRouter(
    tags=["tokens"],
    prefix="/tokens",
)

logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@tokens_router.get("")
async def get_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
