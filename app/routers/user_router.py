import logging
from fastapi import APIRouter
from app.dependencies import SettingsDep
from app.repos import user_repo
from app.schemas import UserRead, UserCreate
from app.db.session import SessionDep, UserDep


users_router = APIRouter(
    tags=["users"],
    prefix="/users",
)

logger = logging.getLogger(__name__)


@users_router.post("",
                   summary="Create a new user",
                   response_model=UserRead,
                   responses={}):
async def create_user(session: SessionDep, user: UserCreate):
    logger.debug(f"Creating user: {user.email}")
    user_repo.create_user(session, user)
    return user
