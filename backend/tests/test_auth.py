"""
Integration tests for the Auth API.
"""

import pytest
import pytest_asyncio


@pytest.mark.asyncio
class TestAuthRegister:
    async def test_register_success(self, client):
        response = await client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "password": "StrongPass123!",
            "full_name": "New User",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "tokens" in data["data"]
        assert "access_token" in data["data"]["tokens"]
        assert data["data"]["user"]["email"] == "newuser@example.com"

    async def test_register_duplicate_email(self, client):
        # First registration
        await client.post("/api/v1/auth/register", json={
            "email": "dupe@example.com",
            "password": "StrongPass123!",
            "full_name": "First User",
        })
        # Duplicate
        response = await client.post("/api/v1/auth/register", json={
            "email": "dupe@example.com",
            "password": "StrongPass123!",
            "full_name": "Second User",
        })
        assert response.status_code == 409

    async def test_register_short_password(self, client):
        response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "short",
            "full_name": "Test User",
        })
        assert response.status_code == 422

    async def test_register_invalid_email(self, client):
        response = await client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "password": "StrongPass123!",
            "full_name": "Test User",
        })
        assert response.status_code == 422


@pytest.mark.asyncio
class TestAuthLogin:
    async def test_login_success(self, client):
        # Register first
        await client.post("/api/v1/auth/register", json={
            "email": "login@example.com",
            "password": "MyPassword123!",
            "full_name": "Login User",
        })
        # Login
        response = await client.post("/api/v1/auth/login", json={
            "email": "login@example.com",
            "password": "MyPassword123!",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]["tokens"]

    async def test_login_wrong_password(self, client):
        await client.post("/api/v1/auth/register", json={
            "email": "wrongpw@example.com",
            "password": "CorrectPass123!",
            "full_name": "Test User",
        })
        response = await client.post("/api/v1/auth/login", json={
            "email": "wrongpw@example.com",
            "password": "WrongPassword!",
        })
        assert response.status_code == 401

    async def test_login_nonexistent_user(self, client):
        response = await client.post("/api/v1/auth/login", json={
            "email": "nobody@example.com",
            "password": "Anything123!",
        })
        assert response.status_code == 401


@pytest.mark.asyncio
class TestAuthMe:
    async def test_get_me(self, client, auth_headers):
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["email"] == "test@example.com"

    async def test_get_me_no_auth(self, client):
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401
