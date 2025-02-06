from functools import lru_cache
from http.client import HTTPException
from typing import Annotated
from app.error.codes import Errors
from app.error.exceptions import AuthenticationException
from sqlalchemy.orm import Session

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import Settings
from app.db.session import get_session

from app.models.user_models import User as UserModel

from app.schemas.user_schemas import User
from app.services.user_service import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@lru_cache
def get_settings():
    return Settings()

def get_current_user(
    db: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    try:
        token_data = verify_token(token, get_settings(), None)
        user = db.query(UserModel).filter(
            UserModel.username == token_data.username).first()
        if user is None:
            raise AuthenticationException(
                error=Errors.E011, code=401)  # User not found
        return user
    except AuthenticationException as e:
        raise HTTPException(
            status_code=e.code,
            detail=Errors.E010,  # Invalid or expired token
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise AuthenticationException(error=Errors.E003, code=400)
    return current_user



SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[User, Depends(get_current_active_user)]

