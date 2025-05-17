import pytest

from hypothesis import given, settings
from hypothesis.strategies import text

from app.core.config import Settings
from app.schemas.token_schemas import TokenCreate, TokenVerify
from app.services.user_service import create_access_token, verify_token


@settings(deadline=None)
@given(text(min_size=1))
def test_token_decode_inverts_encode(username: str):
    settings = Settings()
    token_create = TokenCreate(
        username=username,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    created_token = create_access_token(token_create)

    token_verify = TokenVerify(
        access_token=created_token.access_token,
        token_type=created_token.token_type,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    verified_token = verify_token(token_verify)

    assert username == verified_token.username
