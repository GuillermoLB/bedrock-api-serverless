from functools import lru_cache
from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import Depends

from app.core.config import Settings
from app.db.session import get_session

from app.schemas.user_schemas import User


@lru_cache
def get_settings():
    return Settings()

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise AuthenticationException(error=Errors.E003, code=400)
    return current_user


SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[User, Depends(get_current_active_user)]

