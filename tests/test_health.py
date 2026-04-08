"""
Unit tests for the /health endpoint.
DB calls are mocked so no real database is needed.
Run with: pytest
"""
import pytest
from unittest.mock import patch, MagicMock


# Patch settings before any local imports so db.py doesn't need a real .env
_mock_settings = MagicMock(
    db_host="localhost",
    db_port=5432,
    db_name="testdb",
    db_user="testuser",
    db_password="testpass",
)

with patch("settings.Settings", return_value=_mock_settings), \
     patch("settings.settings", _mock_settings):
    pass  # modules not yet imported; patching happens per-fixture below


@pytest.fixture()
def client():
    with patch("db.settings", _mock_settings), \
         patch("main.run_migrations"), \
         patch("db.create_engine"):
        from main import app
        from fastapi.testclient import TestClient
        with TestClient(app) as c:
            yield c


def test_health_db_up(client):
    with patch("main.ping_db", return_value=True):
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_db_down(client):
    with patch("main.ping_db", return_value=False):
        response = client.get("/health")
    assert response.status_code == 503
    assert response.json()["status"] == "unavailable"
