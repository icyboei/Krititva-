"""
Krititva Web Application
"Architecting Value. Operationalizing Expertise."
Rooted in the Sanskrit concept of कृतित्व (realized output of human intellect and effort).

A SaaS platform that empowers vendors, side hustlers, artisans, craftables sellers,
and service providers to have their own instant micro-storefront profile with transparent
activity charges and an authentic client review and 5-star rating system.
"""

import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

from services.github_service import (
    parse_github_url,
    get_repository_details,
    get_repository_readme,
    get_repository_issues
)
from services.ai_service import generate_issue_roadmap
from services.store import (
    USERS_DB,
    ACTIVITIES_DB,
    REVIEWS_DB,
    INQUIRIES_DB,
    get_user_by_username,
    get_user_by_email,
    authenticate_user,
    register_user,
    get_all_vendors,
    get_vendor_profile,
    get_vendor_listings,
    get_all_listings,
    create_listing,
    add_vendor_review,
    create_inquiry,
    get_vendor_inquiries,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "krititva-dev-secret-key-2026")


@app.context_processor
def inject_context():
    """Injects current logged-in user and all vendors globally into templates."""
    username = session.get("username")
    current_user = get_user_by_username(username) if username else None
    return {
        "current_user": current_user,
        "all_vendors": get_all_vendors()
    }


# =========================================================================
# EXISTING IN-MEMORY ENGAGEMENTS & SPECIALIZED TECHNICAL SERVICES
# =========================================================================

SERVICES_CATALOG = [
    {
        "id": "srv-1",
        "title": "Autonomous AI Agent & Workflow Architecture",
        "provider": {
            "name": "Devratna Joshi",
            "title": "Principal Systems & AI Architect",
            "handle": "@devratna",
            "avatar_initials": "DJ",
            "verified": True,
            "rating": 4.95,
            "completed_engagements": 28,
            "skills": ["Gemma", "Python", "LangChain", "System Architecture"]
        },
        "category": "ai-engineering",
        "description": "Architect and deploy secure, event-driven AI workflow agents with verifiable guardrails and observable tool execution.",
        "deliverables": [
            "Architecture Blueprint & Threat Model",
            "Containerized Flask/FastAPI Service",
            "Automated Evaluation & Benchmark Suite",
            "Deployment Runbook & SLA Documentation"
        ],
        "pricing_type": "Milestone-Based",
        "indicative_pricing": "₹1,50,000 - ₹2,80,000",
        "typical_duration": "2 - 3 Weeks",
        "sla": "48h initial prototype, 99.9% uptime SLA"
    },
    {
        "id": "srv-2",
        "title": "Open-Source Codebase Audit & Security Modernization",
        "provider": {
            "name": "Aanya Sharma",
            "title": "Senior Security Researcher & OSS Maintainer",
            "handle": "@aanyasharma",
            "avatar_initials": "AS",
            "verified": True,
            "rating": 5.0,
            "completed_engagements": 34,
            "skills": ["Python", "Rust", "Static Analysis", "GitHub Security"]
        },
        "category": "security-audit",
        "description": "Comprehensive architectural audit of third-party dependencies, license compliance, CI/CD supply chain risks, and static vulnerability triage.",
        "deliverables": [
            "Executive Vulnerability & License Matrix",
            "Remediation Pull Requests for Critical Findings",
            "Automated Dependency Scanning Pipeline",
            "Maintainer Security Policy (SECURITY.md)"
        ],
        "pricing_type": "Fixed Engagement",
        "indicative_pricing": "₹95,000",
        "typical_duration": "5 Business Days",
        "sla": "Comprehensive report within 72h"
    },
    {
        "id": "srv-3",
        "title": "High-Performance Data Pipeline & BigQuery Engineering",
        "provider": {
            "name": "Kiran Patel",
            "title": "Data Platform Specialist",
            "handle": "@kiranp",
            "avatar_initials": "KP",
            "verified": True,
            "rating": 4.88,
            "completed_engagements": 19,
            "skills": ["BigQuery", "SQL", "dbt", "Cloud Composer"]
        },
        "category": "data-infrastructure",
        "description": "Design cost-optimized BigQuery data transformations, partitioning schemes, and robust dbt orchestration for enterprise scale.",
        "deliverables": [
            "Partitioned & Clustered Data Warehouse Models",
            "dbt Pipeline with Automated Data Quality Tests",
            "Cost Optimization Analysis (30%+ Reduction Target)",
            "Pipeline Monitoring Dashboards"
        ],
        "pricing_type": "Milestone-Based",
        "indicative_pricing": "₹1,80,000 - ₹3,20,000",
        "typical_duration": "3 Weeks",
        "sla": "Zero data-loss guarantee & monitored SLAs"
    }
]

PROJECT_BRIEFS = [
    {
        "id": "brief-1",
        "title": "Secure LLM Gateway Architecture with Token Metering",
        "client_name": "Aura Logistics Inc.",
        "contact_person": "Vikram Seth (VP of Engineering)",
        "category": "ai-engineering",
        "scope": "We require a centralized Python Flask/FastAPI gateway that throttles model queries across departments, audits prompt injections, and logs real-time latency metrics.",
        "budget": "₹1,80,000 - ₹2,50,000",
        "timeline": "2-3 Weeks",
        "status": "Open for Proposals",
        "proposals_count": 3,
        "posted_date": "Oct 15, 2026"
    },
    {
        "id": "brief-2",
        "title": "Open-Source Dependency & License Compliance Audit",
        "client_name": "Zenith FinTech",
        "contact_person": "Priya Nair (Tech Lead)",
        "category": "security-audit",
        "scope": "Audit our backend microservices for copyleft licensing risks (GPL/AGPL) and outdated CVE vulnerabilities before our Series A compliance review.",
        "budget": "₹1,00,000",
        "timeline": "10 Days",
        "status": "Open for Proposals",
        "proposals_count": 2,
        "posted_date": "Oct 16, 2026"
    }
]

ENGAGEMENTS = {
    "eng-8042": {
        "id": "eng-8042",
        "project_title": "Enterprise Knowledge-Base Query Engine with Guardrails",
        "status": "In Progress (Milestone 2)",
        "client": {
            "name": "Aura Logistics Inc.",
            "contact_person": "Vikram Seth (VP of Engineering)",
            "handle": "@vseth_aura",
            "avatar_initials": "AL"
        },
        "provider": {
            "name": "Devratna Joshi",
            "title": "Principal Systems & AI Architect",
            "handle": "@devratna",
            "avatar_initials": "DJ",
            "verified": True
        },
        "total_value": "₹2,60,000",
        "scope_summary": "Design and operationalize a private retrieval pipeline with role-based access control, Gemma integration, and real-time citation validation.",
        "milestones": [
            {
                "id": 1,
                "title": "Architecture Blueprint & Threat Model",
                "due_date": "Completed Oct 12, 2026",
                "amount": "₹80,000",
                "status": "Approved & Released",
                "deliverable": "System Architecture PDF + OpenAPI Specification v1.0",
                "notes": "Reviewed and verified by Aura Logistics VP Engineering on Oct 12."
            },
            {
                "id": 2,
                "title": "Core Retrieval Pipeline & Guardrails Integration",
                "due_date": "Due Oct 22, 2026",
                "amount": "₹1,15,000",
                "status": "In Review",
                "deliverable": "PR #42: Vector Store integration with token verification middleware",
                "notes": "Delivered for review on Oct 16. Pending client sign-off."
            },
            {
                "id": 3,
                "title": "Evaluation Benchmarks & Production Runbook",
                "due_date": "Due Nov 02, 2026",
                "amount": "₹65,000",
                "status": "Upcoming",
                "deliverable": "Automated eval suite with >95% accuracy metric + Dockerized runbook",
                "notes": "Scheduled to begin immediately following Milestone 2 sign-off."
            }
        ],
        "messages": [
            {
                "sender": "client",
                "author": "Vikram Seth (Client)",
                "timestamp": "Oct 16, 10:14 AM",
                "content": "Devratna, we reviewed PR #42 for Milestone 2. The token verification latency looks solid (under 45ms). Testing edge case handling now."
            },
            {
                "sender": "provider",
                "author": "Devratna Joshi (Provider)",
                "timestamp": "Oct 16, 11:30 AM",
                "content": "Thanks Vikram! I added integration tests for token expiration and schema validation in commit 7a8f1b. Ready for milestone sign-off when your team wraps testing."
            }
        ]
    }
}


# =========================================================================
# CORE PAGES & VIEWS
# =========================================================================

@app.route("/")
def index():
    """Renders the main Krititva platform landing page."""
    featured_vendors = get_all_vendors()[:4]
    return render_template("index.html", featured_vendors=featured_vendors)


@app.route("/exchange")
@app.route("/explore")
def exchange():
    """
    Renders the Capabilities & Storefronts Exchange.
    Supports tabs:
    - 'storefronts': Creator & Vendor storefronts with activities and charges
    - 'services': Verified Technical Capabilities Catalog
    - 'briefs': Client Project Briefs
    """
    category = request.args.get("category", "all")
    search_query = request.args.get("q", "").strip().lower()
    default_tab = "storefronts" if request.path == "/explore" else "services"
    tab = request.args.get("tab", default_tab)

    # Filtered Services Catalog
    filtered_services = SERVICES_CATALOG
    if category != "all":
        filtered_services = [s for s in filtered_services if s["category"] == category]
    if search_query:
        filtered_services = [
            s for s in filtered_services
            if search_query in s["title"].lower()
            or search_query in s["description"].lower()
            or search_query in s["provider"]["name"].lower()
            or any(search_query in sk.lower() for sk in s["provider"]["skills"])
        ]

    # Filtered Client Briefs
    filtered_briefs = PROJECT_BRIEFS
    if category != "all":
        filtered_briefs = [b for b in filtered_briefs if b["category"] == category]
    if search_query:
        filtered_briefs = [
            b for b in filtered_briefs
            if search_query in b["title"].lower()
            or search_query in b["scope"].lower()
            or search_query in b["client_name"].lower()
        ]

    # Filtered Vendors & Storefronts
    all_vendors_list = get_all_vendors()
    filtered_vendors = all_vendors_list
    if category != "all":
        filtered_vendors = [v for v in filtered_vendors if category.lower() in v["category"].lower()]
    if search_query:
        filtered_vendors = [
            v for v in filtered_vendors
            if search_query in v["name"].lower()
            or search_query in v["business_name"].lower()
            or search_query in v["category"].lower()
            or search_query in v["tagline"].lower()
            or search_query in v["location"].lower()
            or any(search_query in a["title"].lower() for a in v["activities"])
        ]

    return render_template(
        "exchange.html",
        services=filtered_services,
        briefs=filtered_briefs,
        vendors=filtered_vendors,
        active_category=category,
        active_tab=tab,
        search_query=search_query
    )


@app.route("/profile/<username>")
def vendor_profile(username):
    """
    Renders a dedicated public storefront / profile page for any creator,
    vendor, artisan, or service provider.
    """
    profile = get_vendor_profile(username)
    if not profile:
        return render_template(
            "index.html",
            error=f"Storefront '@{username}' was not found."
        ), 404

    return render_template("profile.html", profile=profile)


@app.route("/dashboard")
def vendor_dashboard():
    """
    Renders the private studio management dashboard for logged-in vendors.
    """
    username = session.get("username")
    user = get_user_by_username(username) if username else None
    vendor_data = get_vendor_profile(username) if user and user.get("role") == "vendor" else None
    inquiries = get_vendor_inquiries(username) if user else []

    return render_template(
        "dashboard.html",
        vendor_data=vendor_data,
        inquiries=inquiries
    )


@app.route("/workspace")
def workspace():
    """Renders the interactive bilateral project engagement workspace."""
    eng_id = request.args.get("id", "eng-8042")
    engagement = ENGAGEMENTS.get(eng_id, ENGAGEMENTS["eng-8042"])
    return render_template("workspace.html", engagement=engagement)


@app.route("/opensource-buddy")
def opensource_buddy():
    """Renders the OpenSource Buddy capability-discovery workbench."""
    return render_template("opensource_buddy.html")


# =========================================================================
# AUTHENTICATION & PERSONA ROUTES
# =========================================================================

@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    """Handles user sign in."""
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "").strip()

        user = authenticate_user(identifier, password)
        if user:
            session["username"] = user["username"]
            if user.get("role") == "vendor":
                return redirect(url_for("vendor_profile", username=user["username"]))
            return redirect(url_for("exchange"))
        else:
            return render_template("auth.html", mode="login", error="Invalid username/email or password.")

    return render_template("auth.html", mode="login")


@app.route("/auth/signup", methods=["GET", "POST"])
def auth_signup():
    """Handles new vendor or client registration."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "vendor").strip()
        business_name = request.form.get("business_name", "").strip()
        category = request.form.get("category", "").strip()
        tagline = request.form.get("tagline", "").strip()
        location = request.form.get("location", "").strip()

        try:
            user = register_user(
                name=name,
                email=email,
                username=username,
                password=password,
                role=role,
                business_name=business_name,
                category=category,
                tagline=tagline,
                location=location
            )
            session["username"] = user["username"]
            if role == "vendor":
                return redirect(url_for("vendor_profile", username=user["username"]))
            return redirect(url_for("exchange"))
        except ValueError as e:
            return render_template("auth.html", mode="signup", error=str(e))

    return render_template("auth.html", mode="signup")


@app.route("/auth/logout")
def auth_logout():
    """Clears user session."""
    session.clear()
    return redirect(url_for("index"))


@app.route("/auth/switch-demo", methods=["POST"])
def auth_switch_demo():
    """Allows one-click switching between pre-seeded demo personas for interactive evaluation."""
    target_username = request.form.get("username") or (request.get_json() or {}).get("username")
    if target_username and target_username in USERS_DB:
        session["username"] = target_username
        user = USERS_DB[target_username]
        if user.get("role") == "vendor":
            return redirect(url_for("vendor_profile", username=target_username))
        return redirect(url_for("exchange"))
    return redirect(url_for("exchange"))


# =========================================================================
# REST APIS FOR LISTINGS, REVIEWS & INQUIRIES
# =========================================================================

@app.route("/api/vendors", methods=["GET"])
def api_get_vendors():
    """Lists all registered vendor profiles."""
    return jsonify(get_all_vendors())


@app.route("/api/vendors/<username>", methods=["GET"])
def api_get_vendor_profile(username):
    """Retrieves full profile for a specific vendor."""
    profile = get_vendor_profile(username)
    if not profile:
        return jsonify({"error": "Vendor not found"}), 404
    return jsonify(profile)


@app.route("/api/listings/create", methods=["POST"])
def api_create_listing():
    """
    Endpoint for a vendor to list a new activity, craft, or service
    with appropriate charges.
    """
    data = request.get_json() or {}
    vendor_username = data.get("vendor_username") or session.get("username")
    if not vendor_username:
        return jsonify({"error": "You must be signed in as a vendor to create a listing."}), 401

    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Activity title is required."}), 400

    charges_display = data.get("charges_display", "").strip()
    if not charges_display:
        return jsonify({"error": "Appropriate charges (pricing) must be specified."}), 400

    try:
        new_listing = create_listing(
            vendor_username=vendor_username,
            title=title,
            category=data.get("category", "Handmade Crafts"),
            charges_display=charges_display,
            charges_amount=data.get("charges_amount", 1000.0),
            pricing_model=data.get("pricing_model", "Fixed Price"),
            turnaround=data.get("turnaround", "3-5 Business Days"),
            description=data.get("description", "Handcrafted artisanal offering."),
            inclusions=data.get("inclusions", []),
            tags=data.get("tags", []),
            type_name=data.get("type_name", "Handmade Craftable"),
            theme_icon=data.get("theme_icon", "✨")
        )
        return jsonify({"status": "success", "listing": new_listing}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/vendors/<username>/review", methods=["POST"])
def api_submit_vendor_review(username):
    """
    Endpoint for clients to post feedback and rate the service provider (1-5 stars).
    Recalculates aggregate rating score and returns updated stats.
    """
    data = request.get_json() or {}
    client_name = data.get("client_name", "").strip()
    review_title = data.get("review_title", "").strip()
    comment = data.get("comment", "").strip()
    rating = data.get("rating")
    activity_title = data.get("activity_title", "Artisanal Service")

    if not client_name:
        return jsonify({"error": "Client name is required."}), 400
    if not review_title:
        return jsonify({"error": "Review headline is required."}), 400
    if not comment:
        return jsonify({"error": "Review feedback comment is required."}), 400
    if rating is None:
        return jsonify({"error": "Rating (1 to 5 stars) is required."}), 400

    try:
        rating_num = float(rating)
    except (ValueError, TypeError):
        return jsonify({"error": "Rating must be a valid number between 1 and 5."}), 400

    try:
        result = add_vendor_review(
            vendor_username=username,
            client_name=client_name,
            rating=rating_num,
            review_title=review_title,
            comment=comment,
            activity_title=activity_title
        )
        return jsonify({
            "status": "success",
            "review": result["review"],
            "new_avg_rating": result["new_avg_rating"],
            "total_reviews": result["total_reviews"],
            "star_breakdown": result["star_breakdown"]
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/api/inquire", methods=["POST"])
def api_submit_inquiry():
    """
    Endpoint for clients to submit an order request or custom commission inquiry.
    """
    data = request.get_json() or {}
    vendor_username = data.get("vendor_username", "").strip()
    client_name = data.get("client_name", "").strip()
    client_email = data.get("client_email", "").strip()
    client_phone = data.get("client_phone", "").strip()
    activity_title = data.get("activity_title", "").strip()
    message = data.get("message", "").strip()

    if not vendor_username or not client_name or not client_email or not message:
        return jsonify({"error": "Vendor, client name, email, and message are required."}), 400

    try:
        inq = create_inquiry(
            vendor_username=vendor_username,
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            activity_title=activity_title,
            message=message
        )
        return jsonify({"status": "success", "inquiry": inq}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# =========================================================================
# EXISTING REST API ENDPOINTS (SERVICES, BRIEFS, WORKSPACE, GITHUB)
# =========================================================================

@app.route("/api/services", methods=["GET", "POST"])
def api_services():
    """List or create capability listings."""
    if request.method == "POST":
        data = request.get_json() or {}
        title = data.get("title", "").strip()
        if not title:
            return jsonify({"error": "Title is required"}), 400

        skills_raw = data.get("skills", ["Specialized Capability"])
        if isinstance(skills_raw, str):
            skills = [s.strip() for s in skills_raw.split(",") if s.strip()]
        else:
            skills = skills_raw

        deliverables_raw = data.get("deliverables", ["Defined Architectural Deliverables"])
        if isinstance(deliverables_raw, str):
            deliverables = [d.strip() for d in deliverables_raw.split("\n") if d.strip()]
        else:
            deliverables = deliverables_raw

        new_service = {
            "id": f"srv-{len(SERVICES_CATALOG) + 1}",
            "title": title,
            "provider": {
                "name": data.get("provider_name", "Prathmesh Ganeshe"),
                "title": data.get("provider_title", "Independent Specialist"),
                "handle": "@" + data.get("provider_name", "user").lower().replace(" ", ""),
                "avatar_initials": "".join([part[0].upper() for part in data.get("provider_name", "PG").split()[:2]]),
                "verified": True,
                "rating": 5.0,
                "completed_engagements": 1,
                "skills": skills or ["Python", "Engineering"]
            },
            "category": data.get("category", "ai-engineering"),
            "description": data.get("description", "Comprehensive, milestone-governed engineering capability."),
            "deliverables": deliverables,
            "pricing_type": data.get("pricing_type", "Milestone-Based"),
            "indicative_pricing": data.get("indicative_pricing", "₹1,20,000"),
            "typical_duration": data.get("typical_duration", "2 Weeks"),
            "sla": data.get("sla", "48h response SLA with verifiable quality standards")
        }
        SERVICES_CATALOG.insert(0, new_service)
        return jsonify({"status": "success", "service": new_service}), 201

    return jsonify(SERVICES_CATALOG)


@app.route("/api/briefs", methods=["GET", "POST"])
def api_briefs():
    """List or create client project briefs."""
    if request.method == "POST":
        data = request.get_json() or {}
        title = data.get("title", "").strip()
        if not title:
            return jsonify({"error": "Brief title is required"}), 400

        new_brief = {
            "id": f"brief-{len(PROJECT_BRIEFS) + 1}",
            "title": title,
            "client_name": data.get("client_name", "Independent Client"),
            "contact_person": data.get("contact_person", "Enterprise Lead"),
            "category": data.get("category", "ai-engineering"),
            "scope": data.get("scope", "Detailed requirements defined in project brief."),
            "budget": data.get("budget", "₹1,50,000"),
            "timeline": data.get("timeline", "2-3 Weeks"),
            "status": "Open for Proposals",
            "proposals_count": 0,
            "posted_date": datetime.now().strftime("%b %d, %Y")
        }
        PROJECT_BRIEFS.insert(0, new_brief)
        return jsonify({"status": "success", "brief": new_brief}), 201

    return jsonify(PROJECT_BRIEFS)


@app.route("/api/engagements/create", methods=["POST"])
def api_create_engagement():
    """Create a new bilateral engagement between a client and a service provider."""
    data = request.get_json() or {}
    service_id = data.get("service_id")
    target_service = next((s for s in SERVICES_CATALOG if s["id"] == service_id), SERVICES_CATALOG[0])

    new_id = f"eng-{uuid.uuid4().hex[:6]}"
    total_val = data.get("budget", target_service["indicative_pricing"])

    new_engagement = {
        "id": new_id,
        "project_title": data.get("title", f"Engagement: {target_service['title']}"),
        "status": "In Progress (Milestone 1)",
        "client": {
            "name": data.get("client_name", "Enterprise Client"),
            "contact_person": data.get("contact_person", "Project Lead"),
            "handle": "@client",
            "avatar_initials": "EC"
        },
        "provider": target_service["provider"],
        "total_value": total_val,
        "scope_summary": data.get("scope", target_service["description"]),
        "milestones": [
            {
                "id": 1,
                "title": "Initial Scoping & Architectural Specification",
                "due_date": "Due in 5 Days",
                "amount": "₹60,000",
                "status": "In Progress",
                "deliverable": "Detailed scope specification & design document",
                "notes": "Initiated upon bilateral agreement."
            },
            {
                "id": 2,
                "title": "Core Implementation & Demonstration",
                "due_date": "Due in 14 Days",
                "amount": "₹90,000",
                "status": "Upcoming",
                "deliverable": "Working repository with integration tests",
                "notes": "Starts after Milestone 1 approval."
            }
        ],
        "messages": [
            {
                "sender": "client",
                "author": f"{data.get('client_name', 'Client')} (Client)",
                "timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
                "content": f"Hello {target_service['provider']['name']}! We've formally commissioned this engagement for {total_val}. Looking forward to the initial scoping delivery."
            }
        ]
    }
    ENGAGEMENTS[new_id] = new_engagement
    return jsonify({"status": "success", "engagement_id": new_id}), 201


@app.route("/api/workspace/message", methods=["POST"])
def api_post_message():
    """Allows client or provider to post a message in the collaborative engagement."""
    data = request.get_json() or {}
    message_text = data.get("content", "").strip()
    sender_role = data.get("role", "client")
    eng_id = data.get("engagement_id", "eng-8042")

    if not message_text:
        return jsonify({"error": "Message content cannot be empty"}), 400

    target_eng = ENGAGEMENTS.get(eng_id, ENGAGEMENTS["eng-8042"])
    author_name = f"{target_eng['client']['contact_person']} (Client)" if sender_role == "client" else f"{target_eng['provider']['name']} (Provider)"

    new_message = {
        "sender": sender_role,
        "author": author_name,
        "timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
        "content": message_text
    }
    target_eng["messages"].append(new_message)
    return jsonify({"status": "success", "message": new_message}), 201


@app.route("/api/workspace/milestone/<int:milestone_id>/approve", methods=["POST"])
def api_approve_milestone(milestone_id):
    """Simulates client milestone approval and release of funds from escrow."""
    eng_id = request.args.get("engagement_id", "eng-8042")
    target_eng = ENGAGEMENTS.get(eng_id, ENGAGEMENTS["eng-8042"])

    for m in target_eng["milestones"]:
        if m["id"] == milestone_id:
            m["status"] = "Approved & Released"
            m["notes"] = f"Approved by Client on {datetime.now().strftime('%b %d, %Y')}."
            return jsonify({"status": "success", "milestone": m})
    return jsonify({"error": "Milestone not found"}), 404


@app.route("/api/workspace/milestone/<int:milestone_id>/submit", methods=["POST"])
def api_submit_milestone_deliverable(milestone_id):
    """Provider action to submit deliverable proof for client review."""
    data = request.get_json() or {}
    eng_id = data.get("engagement_id", "eng-8042")
    target_eng = ENGAGEMENTS.get(eng_id, ENGAGEMENTS["eng-8042"])
    deliverable_link = data.get("deliverable", "https://github.com/pull/1").strip()
    notes = data.get("notes", "Submitted for client verification.")

    for m in target_eng["milestones"]:
        if m["id"] == milestone_id:
            m["status"] = "In Review"
            m["deliverable"] = deliverable_link
            m["notes"] = f"Delivered by Provider on {datetime.now().strftime('%b %d, %Y')}: {notes}"
            target_eng["messages"].append({
                "sender": "provider",
                "author": f"{target_eng['provider']['name']} (Provider)",
                "timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
                "content": f"🚀 Delivered Milestone {milestone_id}: {deliverable_link}. Ready for client review!"
            })
            return jsonify({"status": "success", "milestone": m})
    return jsonify({"error": "Milestone not found"}), 404


@app.route("/api/analyze-repo", methods=["POST"])
def api_analyze_repo():
    """Fetches real repository metadata, README, and open issues from GitHub."""
    data = request.get_json() or {}
    raw_url = data.get("repo_url", "").strip()

    owner, repo = parse_github_url(raw_url)
    if not owner or not repo:
        return jsonify({
            "error": "Invalid GitHub repository URL. Please enter a valid URL like 'https://github.com/owner/repository'."
        }), 400

    try:
        details = get_repository_details(owner, repo)
        readme = get_repository_readme(owner, repo)
        issues = get_repository_issues(owner, repo)

        return jsonify({
            "status": "success",
            "repository": details,
            "readme": readme,
            "issues": issues,
            "issues_count": len(issues)
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve repository data: {str(e)}"}), 500


@app.route("/api/explain-issue", methods=["POST"])
def api_explain_issue():
    """Generates an evidence-backed issue breakdown and contribution roadmap."""
    data = request.get_json() or {}
    issue_data = data.get("issue", {})
    repo_context = data.get("repository", {})

    if not issue_data or not issue_data.get("title"):
        return jsonify({"error": "Issue data with title is required."}), 400

    explanation = generate_issue_roadmap(issue_data, repo_context)
    return jsonify({
        "status": "success",
        "issue_number": issue_data.get("number"),
        "roadmap": explanation
    })


@app.route("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "app": "Krititva", "version": "2.0.0"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1")
    app.run(host="0.0.0.0", port=port, debug=debug)
