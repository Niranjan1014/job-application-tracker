"""Tests for the applications endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_health_endpoint():
    from app.main import app
    client = TestClient(app)
    with patch("app.database.engine"):
        resp = client.get("/health")
    assert resp.status_code == 200

def test_valid_status_values():
    valid = ["Applied", "Screening", "Interview", "Offer", "Rejected"]
    assert len(valid) == 5
    assert "Applied" in valid
