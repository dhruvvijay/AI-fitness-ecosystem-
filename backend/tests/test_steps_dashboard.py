"""
Integration tests for Steps and Dashboard APIs.
"""

import pytest


@pytest.mark.asyncio
class TestStepsAPI:
    async def test_log_steps(self, client, auth_headers):
        response = await client.post(
            "/api/v1/steps",
            json={"steps": 8500, "source": "manual"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["steps"] == 8500

    async def test_get_today(self, client, auth_headers):
        # Log first
        await client.post(
            "/api/v1/steps", json={"steps": 5000}, headers=auth_headers,
        )
        response = await client.get("/api/v1/steps/today", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["data"]["steps"] == 5000

    async def test_upsert_steps(self, client, auth_headers):
        """Logging steps again should update, not duplicate."""
        await client.post("/api/v1/steps", json={"steps": 3000}, headers=auth_headers)
        await client.post("/api/v1/steps", json={"steps": 7000}, headers=auth_headers)

        response = await client.get("/api/v1/steps/today", headers=auth_headers)
        assert response.json()["data"]["steps"] == 7000

    async def test_steps_validation(self, client, auth_headers):
        response = await client.post(
            "/api/v1/steps", json={"steps": -100}, headers=auth_headers,
        )
        assert response.status_code == 422

    async def test_get_week(self, client, auth_headers):
        response = await client.get("/api/v1/steps/week", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 7


@pytest.mark.asyncio
class TestDashboardAPI:
    async def test_dashboard(self, client, auth_headers):
        response = await client.get("/api/v1/dashboard", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert "today" in data
        assert "steps" in data
        assert "calories" in data
        assert "nutrition" in data
        assert "water" in data
        assert "workouts" in data
        assert "targets" in data

    async def test_dashboard_no_auth(self, client):
        response = await client.get("/api/v1/dashboard")
        assert response.status_code == 401


@pytest.mark.asyncio
class TestHealthCheck:
    async def test_health(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["app"] == "AI Fitness Ecosystem"

    async def test_root(self, client):
        response = await client.get("/")
        assert response.status_code == 200
