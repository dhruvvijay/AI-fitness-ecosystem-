"""
Pytest configuration — test fixtures for the AI Fitness Ecosystem.
Uses SQLite in-memory for fast, isolated test execution.
"""

import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db.base import Base, get_db
from app.main import app


# Use SQLite in-memory for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionFactory = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Shared event loop for all tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Create tables before each test, drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session():
    """Yield a test database session."""
    async with TestSessionFactory() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    """Yield an async test client with overridden DB dependency."""
    async def override_get_db():
        try:
            yield db_session
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_headers(client):
    """Register a test user and return auth headers."""
    # Register
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "TestPass123!",
        "full_name": "Test User",
    })
    data = response.json()
    token = data["data"]["tokens"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
