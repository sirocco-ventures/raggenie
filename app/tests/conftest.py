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

# Function to initialize the FastAPI application with all necessary routers
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

# Database URL for testing with SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
# Create a SQLAlchemy engine for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to create a fresh database for each test case
@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, None, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the database tables
    _app = start_application()  # Initialize the FastAPI application
    yield _app  # Yield the application instance for use in tests
    Base.metadata.drop_all(engine)  # Drop the database tables after tests

# Fixture to manage database sessions for tests
@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[Session, None, None]:
    # Connect to the database and begin a transaction for testing
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)  # Create a new session
    yield session  # Yield the session for use in tests
    session.close()  # Close the session after tests
    transaction.rollback()  # Roll back the transaction to maintain isolation
    connection.close()  # Close the database connection

# Fixture to create a FastAPI TestClient for sending requests in tests
@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, None, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    # Override the get_db dependency to use the test database session
    def _get_test_db():
        try:
            yield db_session  # Yield the test database session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db  # Apply the dependency override
    with TestClient(app) as client:
        yield client  # Yield the TestClient for use in tests

# Fixture to create a sample Provider for testing
@pytest.fixture
def provider_fixture(db_session: Session) -> Provider:
    # Sample provider data for creating a Provider instance
    provider_data = {
        "name": "postgres Provider",
        "description": "Provider for postgres connectors",
        "enable": True,
        "icon": "postgres-icon.png",
        "category_id": 2,
        "key": "postgres",
    }
    new_provider = Provider(**provider_data)  # Create a new Provider instance
    db_session.add(new_provider)  # Add the provider to the session
    db_session.commit()  # Commit the session to save the provider
    db_session.refresh(new_provider)  # Refresh the provider instance to get updated data
    return new_provider  # Return the created Provider instance
