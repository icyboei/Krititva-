"""
Unit and integration tests for Krititva web application.
"""

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test health check route."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "ok"
    assert json_data["app"] == "Krititva"


def test_landing_page(client):
    """Test main landing page rendering and core brand headings."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Architecting Value." in html
    assert "Operationalizing Expertise." in html
    assert "Procure" in html
    assert "Commercialize" in html
    assert "OpenSource Buddy" in html


def test_opensource_buddy_route(client):
    """Test OpenSource Buddy view route."""
    response = client.get("/opensource-buddy")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "OpenSource Buddy" in html
    assert "GitHub Repository URL" in html
