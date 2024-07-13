import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_session, Base
from src.auth.service import get_password_hash
from src.auth.models import User

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(scope="module")
async def test_app():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    client = TestClient(app)
    yield client
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="module")
async def session():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="module")
async def test_user(session: AsyncSession):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": get_password_hash("password"),
        "first_name": "Test",
        "role": "user",
        "is_active": True,
        "is_verified": False
    }
    user = User(**user_data)
    session.add(user)
    await session.commit()
    return user

def test_register_user(test_app, session):
    response = test_app.post("/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
        "first_name": "New",
        "role": "user"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_login_user(test_app, test_user):
    response = test_app.post("/auth/login", data={"username": test_user.username, "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_users(test_app, test_user):
    response = test_app.get("/auth/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0
