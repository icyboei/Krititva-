"""
Krititva Web Application
"Architecting Value. Operationalizing Expertise."
Rooted in the Sanskrit concept of कृतित्व.
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "krititva-dev-secret-key-2026")

# In-Memory Store for Interactive Demonstration (Client & Provider Exchange)
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

# Active Demonstration Engagement (Client <-> Provider Collaboration Workspace)
ENGAGEMENT_WORKSPACE = {
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
            "author": "Vikram Seth",
            "timestamp": "Oct 16, 10:14 AM",
            "content": "Devratna, we reviewed PR #42 for Milestone 2. The token verification latency looks solid (under 45ms). Testing edge case handling now."
        },
        {
            "sender": "provider",
            "author": "Devratna Joshi",
            "timestamp": "Oct 16, 11:30 AM",
            "content": "Thanks Vikram! I added integration tests for token expiration and schema validation in commit 7a8f1b. Ready for milestone sign-off when your team wraps testing."
        }
    ]
}


@app.route("/")
def index():
    """Renders the main Krititva platform landing page."""
    return render_template("index.html")


@app.route("/exchange")
def exchange():
    """Renders the bilateral Capability & Services Exchange."""
    category = request.args.get("category", "all")
    filtered_services = SERVICES_CATALOG
    if category != "all":
        filtered_services = [s for s in SERVICES_CATALOG if s["category"] == category]
    return render_template("exchange.html", services=filtered_services, active_category=category)


@app.route("/workspace")
def workspace():
    """Renders the interactive bilateral project engagement workspace."""
    return render_template("workspace.html", engagement=ENGAGEMENT_WORKSPACE)


@app.route("/opensource-buddy")
def opensource_buddy():
    """Renders the OpenSource Buddy capability-discovery workbench."""
    return render_template("opensource_buddy.html")


@app.route("/api/services", methods=["GET", "POST"])
def api_services():
    """List or create capability listings."""
    if request.method == "POST":
        data = request.get_json() or {}
        new_service = {
            "id": f"srv-{len(SERVICES_CATALOG) + 1}",
            "title": data.get("title", "Untitled Capability"),
            "provider": {
                "name": data.get("provider_name", "Anonymous Contributor"),
                "title": data.get("provider_title", "Technical Specialist"),
                "handle": "@" + data.get("provider_name", "user").lower().replace(" ", ""),
                "avatar_initials": "".join([part[0].upper() for part in data.get("provider_name", "TS").split()[:2]]),
                "verified": True,
                "rating": 5.0,
                "completed_engagements": 1,
                "skills": data.get("skills", ["General Capability"])
            },
            "category": data.get("category", "general"),
            "description": data.get("description", ""),
            "deliverables": data.get("deliverables", ["Defined Milestone Deliverables"]),
            "pricing_type": data.get("pricing_type", "Milestone-Based"),
            "indicative_pricing": data.get("indicative_pricing", "Quote-Based"),
            "typical_duration": data.get("typical_duration", "Flexible"),
            "sla": data.get("sla", "Standard Response SLA")
        }
        SERVICES_CATALOG.insert(0, new_service)
        return jsonify({"status": "success", "service": new_service}), 201
    return jsonify(SERVICES_CATALOG)


@app.route("/api/workspace/message", methods=["POST"])
def api_post_message():
    """Allows client or provider to post a message in the collaborative engagement."""
    data = request.get_json() or {}
    message_text = data.get("content", "").strip()
    sender_role = data.get("role", "client")
    
    if not message_text:
        return jsonify({"error": "Message content cannot be empty"}), 400

    author_name = "Vikram Seth (Client)" if sender_role == "client" else "Devratna Joshi (Provider)"
    new_message = {
        "sender": sender_role,
        "author": author_name,
        "timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
        "content": message_text
    }
    ENGAGEMENT_WORKSPACE["messages"].append(new_message)
    return jsonify({"status": "success", "message": new_message}), 201


@app.route("/api/workspace/milestone/<int:milestone_id>/approve", methods=["POST"])
def api_approve_milestone(milestone_id):
    """Simulates client milestone approval and release of funds."""
    for m in ENGAGEMENT_WORKSPACE["milestones"]:
        if m["id"] == milestone_id:
            m["status"] = "Approved & Released"
            m["notes"] = f"Approved by Client on {datetime.now().strftime('%b %d, %Y')}."
            return jsonify({"status": "success", "milestone": m})
    return jsonify({"error": "Milestone not found"}), 404


@app.route("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "app": "Krititva", "version": "1.1.0"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1")
    app.run(host="0.0.0.0", port=port, debug=debug)
