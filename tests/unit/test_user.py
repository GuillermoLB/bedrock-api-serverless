from app.repos import user_repo
from app.schemas.user_schemas import UserCreate
import pytest


def test_create_user_works(session):
    new_user = UserCreate(username="test_user", password="test_password")
    user = user_repo.create_user(session, new_user)
    assert user.username == "test_user"
