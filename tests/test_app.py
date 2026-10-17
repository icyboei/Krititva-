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


def test_exchange_briefs_tab(client):
    """Test exchange project briefs tab."""
    response = client.get("/exchange?tab=briefs")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Open Client Project Briefs" in html
    assert "Aura Logistics Inc." in html


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


def test_api_create_brief(client):
    """Test posting a new project brief."""
    payload = {
        "title": "Automated Code Review Agent",
        "client_name": "Acme Ventures",
        "category": "ai-engineering",
        "scope": "Develop a PR bot that comments on architectural violations.",
        "budget": "₹1,20,000",
        "timeline": "2 Weeks"
    }
    response = client.post("/api/briefs", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["brief"]["title"] == "Automated Code Review Agent"


def test_api_create_engagement(client):
    """Test creating an active engagement from a service listing."""
    payload = {
        "service_id": "srv-1",
        "title": "Custom AI Agent System",
        "client_name": "Starlight Corp",
        "budget": "₹2,00,000",
        "scope": "Integrate Gemma with internal CRM database."
    }
    response = client.post("/api/engagements/create", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert "engagement_id" in data


def test_api_submit_milestone_deliverable(client):
    """Test provider submitting a deliverable for an active milestone."""
    payload = {
        "engagement_id": "eng-8042",
        "deliverable": "https://github.com/icyboei/krititva/pull/1",
        "notes": "Added integration tests and documentation."
    }
    response = client.post("/api/workspace/milestone/3/submit", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["milestone"]["status"] == "In Review"


def test_api_approve_milestone(client):
    """Test client approving milestone and releasing funds."""
    response = client.post("/api/workspace/milestone/2/approve?engagement_id=eng-8042")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["milestone"]["status"] == "Approved & Released"


def test_api_explain_issue(client):
    """Test issue explanation AI endpoint."""
    payload = {
        "issue": {
            "number": 12,
            "title": "Add retry mechanism for network timeouts",
            "body": "Connections drop when remote host is throttled.",
            "labels": [{"name": "enhancement"}]
        },
        "repository": {
            "name": "krititva",
            "language": "Python"
        }
    }
    response = client.post("/api/explain-issue", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "roadmap" in data
