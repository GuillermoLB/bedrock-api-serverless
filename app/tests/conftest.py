import os
import pathlib
from typing import AsyncGenerator

import boto3
from app.tests.mocks.mock_bedrock import mock_bedrock_make_api_call
from moto import mock_aws
from app.core.config import Settings
from app.db.session import get_session
from app.models.user_models import Base, User
from fastapi import FastAPI
from httpx import AsyncClient
from factory.alchemy import SQLAlchemyModelFactory
import pytest_asyncio
import pytest
from unittest.mock import patch
import psycopg2
from alembic import command
from alembic.config import Config

from sqlalchemy import UUID, Engine, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.database import database, password, port, server, user
from app.dependencies import get_bedrock, get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings = get_settings()
    settings.POSTGRES_DB = "postgres_tests"
    return settings


@pytest.fixture(scope="session")
def engine(settings: Settings) -> Engine:
    engine = create_engine(settings.get_connection_str())
    params = {
        "database": database,
        "user": user,
        "password": password,
        "host": server,
        "port": port,
    }

    # Connect to the default database
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cursor = conn.cursor()

    # Create the test database
    print("*****************************************************************************Creating test database...")
    cursor.execute("DROP DATABASE IF EXISTS postgres_tests")
    cursor.execute("CREATE DATABASE postgres_tests")

    # Connect to the test database
    params["database"] = "postgres_tests"
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cursor = conn.cursor()

    return engine


@pytest.fixture(scope="session")
def tables(engine, settings: Settings):
    # Drop all tables if they exist
    Base.metadata.drop_all(engine)

    # Create all tables
    # Base.metadata.create_all(engine)

    # Run Alembic migrations
    alembic_cfg = Config(
        pathlib.Path(__file__).parent.parent.parent.joinpath("alembic.ini")
    )
    alembic_cfg.set_main_option(
        "sqlalchemy.url", settings.get_connection_str())
    command.upgrade(alembic_cfg, "head")

    yield

    Base.metadata.drop_all(engine)


scopedsession = scoped_session(sessionmaker())


@pytest.fixture
def session(engine: Engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = scopedsession(autoflush=False, bind=connection)
    session.begin_nested()
    yield session
    transaction.rollback()
    # session.close()
    scopedsession.remove()

region_name = "eu-central-1"

@pytest.fixture(name="aws_credentials", scope="session")
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = region_name
    os.environ["AWS_SESSION_TOKEN"] = "testing"


with mock_aws():
    moto_s3 = boto3.client("s3", region_name=region_name)

@pytest.fixture(name="bedrock", scope="session")
def bedrock(aws_credentials):
    # Change to bedrock-agent-runtime instead of bedrock
    bedrock_client = boto3.client("bedrock-agent-runtime", region_name=region_name)
    with patch(
        "botocore.client.BaseClient._make_api_call", new=mock_bedrock_make_api_call
    ):
        yield bedrock_client


@pytest_asyncio.fixture()
async def app(session, settings) -> FastAPI:
    from app.main import app

    def get_bedrock_override():
        return bedrock

    def get_session_override():
        return session

    def get_settings_override():
        return settings

    app.dependency_overrides[get_bedrock] = get_bedrock_override
    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_settings] = get_settings_override

    yield app

    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def client(app) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = scopedsession
        sqlalchemy_session_persistence = "flush"
    username = "test_user"
    hashed_password = "test_password"
    disabled = False
