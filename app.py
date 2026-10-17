"""
Krititva Web Application
"Architecting Value. Operationalizing Expertise."
Rooted in the Sanskrit concept of कृतित्व.
"""

import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

from services.github_service import (
    parse_github_url,
    get_repository_details,
    get_repository_readme,
    get_repository_issues
)
from services.ai_service import generate_issue_roadmap

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "krititva-dev-secret-key-2026")

# In-Memory Store: Services Catalog (Capabilities offered by providers)
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

# In-Memory Store: Project Briefs posted by Clients
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

# In-Memory Store: Active Bilateral Engagements
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


@app.route("/")
def index():
    """Renders the main Krititva platform landing page."""
    return render_template("index.html")


@app.route("/exchange")
def exchange():
    """Renders the bilateral Capability & Services Exchange."""
    category = request.args.get("category", "all")
    search_query = request.args.get("q", "").strip().lower()
    tab = request.args.get("tab", "services")  # 'services' or 'briefs'

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

    return render_template(
        "exchange.html",
        services=filtered_services,
        briefs=filtered_briefs,
        active_category=category,
        active_tab=tab,
        search_query=search_query
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


# ==========================================
# REST API ENDPOINTS FOR EXCHANGE & WORKSPACE
# ==========================================

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
    """Provider action to submit deliverable proof (PR link, doc) for client review."""
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
            # Add audit log to chat
            target_eng["messages"].append({
                "sender": "provider",
                "author": f"{target_eng['provider']['name']} (Provider)",
                "timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
                "content": f"🚀 Delivered Milestone {milestone_id}: {deliverable_link}. Ready for client review!"
            })
            return jsonify({"status": "success", "milestone": m})
    return jsonify({"error": "Milestone not found"}), 404


# ==========================================
# OPENSOURCE BUDDY REPO & AI API ENDPOINTS
# ==========================================

@app.route("/api/analyze-repo", methods=["POST"])
def api_analyze_repo():
    """Fetches real repository metadata, README, and open issues from GitHub."""
    data = request.get_json() or {}
    raw_url = data.get("repo_url", "").strip()

    owner, repo = parse_github_url(raw_url)
    if not owner or not repo:
        return jsonify({
            "error": "Invalid GitHub repository URL. Please enter a valid URL like 'https://github.com/owner/repository' or 'owner/repository'."
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
    return {"status": "ok", "app": "Krititva", "version": "1.2.0"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1")
    app.run(host="0.0.0.0", port=port, debug=debug)
