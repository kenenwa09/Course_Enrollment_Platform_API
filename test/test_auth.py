import pytest

@pytest.mark.asyncio
async def test_register_success(client):
    result = await client.post("/api/v1/auth/register", json={
        "name": "John Doe", "email": "john@test.com",
        "password": "securepass", "role": "student"
    })
    assert result.status_code == 201
    data = result.json()
    assert data["email"] == "john@test.com"
    assert data["role"] == "student"
    assert "hashed_password" not in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {"name": "Jane", "email": "jane@test.com", "password": "pass1234", "role": "student"}
    await client.post("/api/v1/auth/register", json=payload)
    result = await client.post("/api/v1/auth/register", json=payload)
    assert result.status_code == 400
    assert "already registered" in result.json()["detail"]

@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/v1/auth/register", json={
        "name": "Jane", "email": "jane@test.com", "password": "pass1234", "role": "student"
    })
    result = await client.post("/api/v1/auth/login", json={
        "email": "jane@test.com", "password": "pass1234"
    })
    assert result.status_code == 200
    assert "access_token" in result.json()

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/api/v1/auth/register", json={
        "name": "Jane", "email": "jane@test.com", "password": "pass1234", "role": "student"
    })
    res = await client.post("/api/v1/auth/login", json={
        "email": "jane@test.com", "password": "wrongpass"
    })
    assert res.status_code == 401

@pytest.mark.asyncio
async def test_get_me(client, student_token):
    res = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {student_token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "student@test.com"

@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    res = await client.get("/api/v1/auth/me")
    assert res.status_code == 401