import pytest
from httpx import AsyncClient

@pytest.mark.asyncio(loop_scope="session")
async def test_root(client: AsyncClient):
    """Test the root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "TAP API is running",
        "version": "1.0.0"
    }

@pytest.mark.asyncio(loop_scope="session")
async def test_health_detailed(client: AsyncClient):
    """Test the detailed health check endpoint."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "components" in data
    assert data["components"]["api"] == "operational"
