"""
GitHub Service
Handles GitHub REST API v3 interactions: repository metadata, README, and open issues.
Treats all external content as untrusted and handles API rate limits/errors safely.
"""

import os
import re
import base64
import requests
from typing import Dict, Any, List, Optional, Tuple

GITHUB_API_BASE = "https://api.github.com"
REQUEST_TIMEOUT = 10  # seconds


def parse_github_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts (owner, repo) from a GitHub URL or 'owner/repo' string.
    Returns (None, None) if the format is invalid.
    """
    if not url:
        return None, None

    cleaned = url.strip().rstrip("/")
    # Handle formats like https://github.com/owner/repo or github.com/owner/repo
    pattern = r"^(?:https?:\/\/)?(?:www\.)?github\.com\/([a-zA-Z0-9_\-\.]+)\/([a-zA-Z0-9_\-\.]+)(?:\.git)?$"
    match = re.match(pattern, cleaned)
    if match:
        owner, repo = match.groups()
        if repo.endswith(".git"):
            repo = repo[:-4]
        return owner, repo

    # Handle 'owner/repo' shorthand
    short_pattern = r"^([a-zA-Z0-9_\-\.]+)\/([a-zA-Z0-9_\-\.]+)$"
    short_match = re.match(short_pattern, cleaned)
    if short_match:
        owner, repo = short_match.groups()
        if repo.endswith(".git"):
            repo = repo[:-4]
        return owner, repo

    return None, None


def _get_headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Krititva-OpenSource-Buddy/1.0"
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def get_repository_details(owner: str, repo: str) -> Dict[str, Any]:
    """
    Fetches real repository metadata from GitHub REST API.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    response = requests.get(url, headers=_get_headers(), timeout=REQUEST_TIMEOUT)

    if response.status_code == 404:
        raise ValueError(f"Repository '{owner}/{repo}' was not found on GitHub.")
    if response.status_code == 403:
        raise PermissionError("GitHub API rate limit exceeded or access forbidden. Try again shortly or supply a GITHUB_TOKEN.")
    if not response.ok:
        raise RuntimeError(f"GitHub API error (HTTP {response.status_code}): {response.text}")

    data = response.json()
    return {
        "owner": data.get("owner", {}).get("login", owner),
        "name": data.get("name", repo),
        "full_name": data.get("full_name", f"{owner}/{repo}"),
        "html_url": data.get("html_url"),
        "description": data.get("description") or "No description provided.",
        "language": data.get("language") or "General",
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues_count": data.get("open_issues_count", 0),
        "default_branch": data.get("default_branch", "main"),
        "license": (data.get("license") or {}).get("name", "Unspecified License"),
        "archived": data.get("archived", False)
    }


def get_repository_readme(owner: str, repo: str) -> str:
    """
    Fetches repository README content and decodes it safely.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme"
    try:
        response = requests.get(url, headers=_get_headers(), timeout=REQUEST_TIMEOUT)
        if response.status_code == 404:
            return "No README file found in this repository."
        if not response.ok:
            return "Unable to fetch README at this time."

        data = response.json()
        content_b64 = data.get("content", "")
        if content_b64:
            decoded = base64.b64decode(content_b64).decode("utf-8", errors="replace")
            # Truncate preview if extremely large
            if len(decoded) > 10000:
                decoded = decoded[:10000] + "\n\n... *(README preview truncated for readability)*"
            return decoded
        return "Empty README file."
    except Exception as e:
        return f"Error retrieving README: {str(e)}"


def get_repository_issues(owner: str, repo: str, label_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetches genuine open issues from GitHub REST API, explicitly excluding Pull Requests.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    params = {
        "state": "open",
        "per_page": 20,
        "sort": "updated",
        "direction": "desc"
    }
    if label_filter and label_filter != "all":
        params["labels"] = label_filter

    response = requests.get(url, headers=_get_headers(), params=params, timeout=REQUEST_TIMEOUT)
    if not response.ok:
        return []

    raw_items = response.json()
    clean_issues = []

    for item in raw_items:
        # Crucial: Exclude pull requests (GitHub issues API returns PRs unless filtered)
        if "pull_request" in item:
            continue

        labels = [
            {"name": l.get("name", ""), "color": l.get("color", "cccccc")}
            for l in item.get("labels", [])
        ]

        body = item.get("body") or "No description provided by the issue author."
        body_preview = body[:240] + ("..." if len(body) > 240 else "")

        clean_issues.append({
            "id": item.get("id"),
            "number": item.get("number"),
            "title": item.get("title", "Untitled Issue"),
            "html_url": item.get("html_url"),
            "comments_count": item.get("comments", 0),
            "created_at": (item.get("created_at") or "")[:10],
            "labels": labels,
            "body": body,
            "body_preview": body_preview,
            "is_good_first_issue": any(
                "first" in l.get("name", "").lower() or "beginner" in l.get("name", "").lower()
                for l in labels
            ),
            "is_help_wanted": any(
                "help" in l.get("name", "").lower()
                for l in labels
            )
        })

    return clean_issues
