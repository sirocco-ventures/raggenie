from typing import Generator, Any
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.models.provider import Provider
from app.utils.database import Base
from app.utils.database import get_db
from app.api.v1.provider import router
from app.api.v1.llmchat import chat_router
from app.api.v1.connector import router as ConnectorRouter
from app.api.v1.connector import cap_router as capabilityrouter
from app.api.v1.connector import inference_router as inference_router
from app.api.v1.connector import actions as actions
from app.api.v1.main_router import MainRouter
from app.api.v1.provider import sample as sample_sql

def start_application() -> FastAPI:
    app = FastAPI()
    app.include_router(MainRouter, prefix="/api/v1/query")
    app.include_router(router, prefix="/api/v1/provider")
    app.include_router(chat_router, prefix="/api/v1/chat")
    app.include_router(capabilityrouter, prefix="/api/v1/capability")
    app.include_router(inference_router, prefix="/api/v1/inference")
    app.include_router(ConnectorRouter, prefix="/api/v1/connector")
    app.include_router(actions, prefix="/api/v1/actions")
    app.include_router(sample_sql, prefix="/api/v1/sql")

    return app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, None, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create tables in the test database
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)  # Optionally drop tables after tests

@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, None, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client

@pytest.fixture
def provider_fixture(db_session: Session) -> Provider:
    provider_data = {
        "name": "postgres Provider",
        "description": "Provider for postgres connectors",
        "enable": True,
        "icon": "postgres-icon.png",
        "category_id": 2,
        "key": "postgres",
    }
    new_provider = Provider(**provider_data)
    db_session.add(new_provider)
    db_session.commit()
    db_session.refresh(new_provider)
    return new_provider
