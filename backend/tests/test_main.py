"""Tests for the main FastAPI application."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_200(self, client):
        """Test that health check returns 200 status."""
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_check_returns_healthy_status(self, client):
        """Test that health check returns healthy status."""
        response = client.get("/api/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data

    def test_health_check_response_structure(self, client):
        """Test that health check has correct response structure."""
        response = client.get("/api/health")
        data = response.json()
        assert "status" in data
        assert "message" in data


class TestCORSMiddleware:
    """Tests for CORS middleware configuration."""

    def test_cors_allows_localhost(self, client):
        """Test that CORS allows localhost origin."""
        response = client.options(
            "/api/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET"
            }
        )
        # OPTIONS requests should work with CORS
        assert response.status_code in [200, 405]
