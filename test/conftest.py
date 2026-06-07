import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.db_async import Base
from app.core.deps import get_db
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def student_token(client):
    await client.post("/api/v1/auth/register", json={
        "name": "Test Student", "email": "student@test.com",
        "password": "password123", "role": "student"
    })
    res = await client.post("/api/v1/auth/login", json={
        "email": "student@test.com", "password": "password123"
    })
    return res.json()["access_token"]

@pytest_asyncio.fixture
async def admin_token(client):
    await client.post("/api/v1/auth/register", json={
        "name": "Admin User", "email": "admin@test.com",
        "password": "password123", "role": "admin"
    })
    res = await client.post("/api/v1/auth/login", json={
        "email": "admin@test.com", "password": "password123"
    })
    return res.json()["access_token"]

@pytest_asyncio.fixture
async def sample_course(client, admin_token):
    res = await client.post("/api/v1/course/", json={
        "title": "Intro to Python", "code": "PY101", "capacity": 30
    }, headers={"Authorization": f"Bearer {admin_token}"})
    return res.json()