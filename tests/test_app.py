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


def test_exchange_marketplace(client):
    """Test exchange marketplace rendering and category filters."""
    response = client.get("/exchange")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Capabilities &amp; Services Exchange" in html or "Capabilities & Services Exchange" in html
    assert "Devratna Joshi" in html
    assert "Post a Project Brief" in html
    assert "List Your Capability" in html


def test_collaboration_workspace(client):
    """Test bilateral collaboration workspace with milestones and chat."""
    response = client.get("/workspace")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Enterprise Knowledge-Base Query Engine" in html
    assert "Aura Logistics Inc." in html
    assert "Devratna Joshi" in html
    assert "Engagement Milestones" in html
    assert "Bilateral Collaboration" in html


def test_api_post_message(client):
    """Test bilateral messaging between client and provider."""
    payload = {
        "role": "client",
        "content": "Automated verification test message from test suite."
    }
    response = client.post("/api/workspace/message", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["message"]["author"] == "Vikram Seth (Client)"


def test_api_approve_milestone(client):
    """Test client approving milestone and releasing funds."""
    response = client.post("/api/workspace/milestone/2/approve")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["milestone"]["status"] == "Approved & Released"
