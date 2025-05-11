from uuid import uuid4
from app.error.exceptions import UserException
from app.repos import user_repo
from app.schemas.user_schemas import UserCreate
import pytest

from app.tests.conftest import UserFactory, session


def test_create_user_works(session):
    new_user = UserCreate(username="test_user", password="test_password")
    user = user_repo.create_user(session, new_user)
    assert user.username == "test_user"

def test_create_existing_user_fails(session):
    UserFactory(username="existing_user")
    new_user = UserCreate(username="existing_user", password="test_password")
    with pytest.raises(UserException, match="E008"):
        user_repo.create_user(session=session, user=new_user)