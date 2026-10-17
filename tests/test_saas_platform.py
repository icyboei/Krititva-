"""
Unit & Integration Tests for Krititva SaaS Micro-Storefront Platform
Validating:
- Authentication & Registration (Vendors & Clients)
- Vendor Profiles & Micro-Storefronts
- Business Activity Listings with Appropriate Charges
- Client Review & 5-Star Rating System
- Customer Inquiries & Studio Dashboard
"""

import pytest
from app import app
from services.store import USERS_DB, ACTIVITIES_DB, REVIEWS_DB, get_vendor_profile


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_vendor_profile_view(client):
    """Test public storefront profile rendering with activities and charges."""
    response = client.get("/profile/maya-ceramics")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Mitti &amp; Clay Studio" in html or "Mitti & Clay Studio" in html
    assert "Maya Sharma" in html
    assert "Hand-Thrown Terracotta Coffee Mugs" in html
    assert "₹1,250" in html
    assert "Client Reviews &amp; Ratings" in html or "Client Reviews & Ratings" in html


def test_auth_login_success(client):
    """Test authenticating with valid credentials."""
    response = client.post("/auth/login", data={
        "identifier": "maya-ceramics",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Mitti &amp; Clay Studio" in html or "Mitti & Clay Studio" in html


def test_auth_login_invalid(client):
    """Test login failure with wrong password."""
    response = client.post("/auth/login", data={
        "identifier": "maya-ceramics",
        "password": "wrongpassword"
    })
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Invalid username/email or password" in html


def test_auth_signup_vendor(client):
    """Test registering a new vendor storefront."""
    username = "test-pottery-studio"
    email = "test.potter@example.com"
    payload = {
        "name": "Kavita Rao",
        "username": username,
        "email": email,
        "password": "password123",
        "role": "vendor",
        "business_name": "Kavita Ceramics",
        "category": "Handmade Crafts & Pottery",
        "tagline": "Organic hand-glazed porcelain and earthen wares",
        "location": "Pune, Maharashtra"
    }
    response = client.post("/auth/signup", data=payload, follow_redirects=True)
    assert response.status_code == 200
    assert username in USERS_DB
    assert USERS_DB[username]["business_name"] == "Kavita Ceramics"


def test_auth_switch_demo(client):
    """Test 1-click demo persona switcher."""
    response = client.post("/auth/switch-demo", data={
        "username": "rohan-leather"
    }, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Heritage Tannery &amp; Goods" in html or "Heritage Tannery & Goods" in html


def test_api_submit_vendor_review(client):
    """Test client submitting a rating and review for a vendor."""
    payload = {
        "client_name": "Vikram Adve",
        "rating": 5,
        "review_title": "Remarkable clay work and prompt shipping",
        "comment": "The mugs arrived intact and look even better than photos. Smooth clay texture!",
        "activity_title": "Hand-Thrown Terracotta Coffee Mugs"
    }
    response = client.post("/api/vendors/maya-ceramics/review", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["review"]["client_name"] == "Vikram Adve"
    assert data["review"]["rating"] == 5
    assert "new_avg_rating" in data
    assert data["total_reviews"] >= 1


def test_api_create_listing_with_charges(client):
    """Test vendor creating a new listing with charges and turnaround schedule."""
    # Authenticate as vendor
    with client.session_transaction() as sess:
        sess["username"] = "maya-ceramics"

    payload = {
        "vendor_username": "maya-ceramics",
        "title": "Rustic Speckled Pasta Bowls (Set of 4)",
        "category": "Handmade Crafts & Pottery",
        "charges_display": "₹2,800",
        "charges_amount": 2800,
        "pricing_model": "Set of 4 Bowls",
        "turnaround": "Handcrafted in 5 Days",
        "description": "Wide-rimmed stoneware bowls designed for hearty pastas and grain salads.",
        "inclusions": ["4x Stoneware pasta bowls", "High-fire food-safe glaze"]
    }
    response = client.post("/api/listings/create", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["listing"]["title"] == "Rustic Speckled Pasta Bowls (Set of 4)"
    assert data["listing"]["charges_display"] == "₹2,800"

    # Verify listing is visible on public profile
    prof_resp = client.get("/profile/maya-ceramics")
    assert "Rustic Speckled Pasta Bowls (Set of 4)" in prof_resp.get_data(as_text=True)


def test_api_submit_inquiry(client):
    """Test submitting an inquiry/order to a vendor."""
    payload = {
        "vendor_username": "maya-ceramics",
        "client_name": "Anita Desai",
        "client_email": "anita.desai@gmail.com",
        "client_phone": "+91 99887 76655",
        "activity_title": "Hand-Thrown Terracotta Coffee Mugs",
        "message": "Hi Maya, looking to order 10 sets as wedding favors. Can you share bulk timeline?"
    }
    response = client.post("/api/inquire", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["inquiry"]["client_name"] == "Anita Desai"


def test_vendor_dashboard(client):
    """Test vendor accessing private dashboard."""
    with client.session_transaction() as sess:
        sess["username"] = "maya-ceramics"

    response = client.get("/dashboard")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Mitti &amp; Clay Studio" in html or "Mitti & Clay Studio" in html
    assert "My Listed Activities" in html
    assert "Customer Inquiries" in html
