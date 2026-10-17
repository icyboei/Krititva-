"""
Unit tests for GitHub service functions.
"""

from services.github_service import parse_github_url
from services.ai_service import generate_issue_roadmap


def test_parse_github_url_valid():
    """Verify various valid GitHub repository URLs are correctly parsed."""
    assert parse_github_url("https://github.com/pallets/flask") == ("pallets", "flask")
    assert parse_github_url("http://github.com/psf/requests/") == ("psf", "requests")
    assert parse_github_url("pallets/flask") == ("pallets", "flask")
    assert parse_github_url("https://github.com/icyboei/krititva.git") == ("icyboei", "krititva")


def test_parse_github_url_invalid():
    """Verify invalid URLs return (None, None)."""
    assert parse_github_url("") == (None, None)
    assert parse_github_url("not-a-url") == (None, None)
    assert parse_github_url("https://gitlab.com/user/project") == (None, None)


def test_ai_roadmap_generation():
    """Verify issue roadmap generator creates structured sections."""
    issue = {
        "number": 101,
        "title": "Fix memory leak in background worker task",
        "body": "When tasks run for over 1 hour, memory consumption spikes indefinitely.",
        "labels": [{"name": "bug", "color": "d73a4a"}]
    }
    repo = {"name": "flask", "language": "Python"}
    result = generate_issue_roadmap(issue, repo)
    assert "explanation_markdown" in result
    assert "What This Issue Appears to Be Asking For" in result["explanation_markdown"]
    assert "Contribution Roadmap" in result["explanation_markdown"]
