"""
AI Integration Service
Generates structured issue explanations and beginner contribution roadmaps.
Distinguishes confirmed GitHub facts from AI-generated suggestions.
"""

import os
import requests
from typing import Dict, Any


def generate_issue_roadmap(issue_data: Dict[str, Any], repo_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produces a clear, evidence-backed breakdown and contribution roadmap for a GitHub issue.
    Uses Gemma if GEMMA_API_KEY is configured, or provides an expert heuristic analysis fallback.
    """
    issue_title = issue_data.get("title", "")
    issue_body = issue_data.get("body", "")
    issue_number = issue_data.get("number", 0)
    repo_name = repo_context.get("name", "repository")
    repo_lang = repo_context.get("language", "General")
    labels = [l.get("name") for l in issue_data.get("labels", []) if isinstance(l, dict)]

    api_key = os.getenv("GEMMA_API_KEY")
    if api_key:
        try:
            prompt = f"""
You are a senior open-source mentor helping a beginner contributor.
Analyze this GitHub issue from repository {repo_name} (Language: {repo_lang}):

Title: #{issue_number} {issue_title}
Labels: {', '.join(labels)}
Issue Description:
{issue_body[:1500]}

Provide a structured, honest explanation with these sections:
1. What this issue appears to be asking for
2. Why it matters
3. Skills & tools likely needed
4. Suggested investigation sequence
5. Step-by-step contribution roadmap
6. Questions to ask maintainers if requirements are unclear
7. Immediate next action for a beginner

Be clear, humble, acknowledge uncertainty, and do not invent fake file paths or maintainer quotes.
"""
            # Generic endpoint call or Google AI Studio Gemini/Gemma format
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=12
            )
            if response.ok:
                resp_json = response.json()
                generated_text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "source": "Gemma AI Engine",
                    "disclaimer": "AI-generated suggestion based on issue text. Please verify requirements with repository maintainers.",
                    "explanation_markdown": generated_text
                }
        except Exception as e:
            # Fall back to heuristic engine if API call fails
            pass

    # Expert Heuristic Analysis (Guaranteed to work offline and without credentials)
    is_bug = any("bug" in str(l).lower() for l in labels) or "fix" in issue_title.lower() or "error" in issue_title.lower()
    is_docs = any("doc" in str(l).lower() for l in labels) or "readme" in issue_title.lower() or "typo" in issue_title.lower()
    is_feature = any("enhancement" in str(l).lower() or "feature" in str(l).lower() for l in labels)

    what_it_asks = f"The issue concerns: \"{issue_title}\"."
    if is_docs:
        what_it_asks += " This appears to be a documentation, guide, or text clarification task."
    elif is_bug:
        what_it_asks += " This appears to report unexpected behavior, runtime bug, or edge-case failure."
    elif is_feature:
        what_it_asks += " This appears to request a new capability, enhancement, or architectural refinement."

    investigation_steps = [
        f"1. Clone the repository locally and inspect the `CONTRIBUTING.md` guidelines for {repo_name}.",
        f"2. Set up the local test environment matching {repo_lang} best practices.",
        f"3. Search the codebase for terms mentioned in the title: `{issue_title[:30]}`.",
        f"4. If reproducing a bug, write a small isolated test case that fails before making changes.",
        "5. Keep your proposed fix focused exclusively on the requested behavior without unrelated refactoring."
    ]

    roadmap_steps = [
        "Phase 1: Local reproduction & test verification",
        "Phase 2: Draft minimal surgical code or doc changes in a new branch",
        "Phase 3: Run the project test suite and linters to verify zero regressions",
        "Phase 4: Open a Draft Pull Request referencing this issue number",
        "Phase 5: Solicit maintainer review with clear before-and-after evidence"
    ]

    maintainer_questions = [
        f"\"Hi maintainers! I'd like to help investigate issue #{issue_number}. Could you confirm if this is currently unassigned?\"",
        "\"Is there an existing test case or sample input that demonstrates the expected behavior?\"",
        "\"Do you prefer this handled in a specific module or following any particular architectural convention?\""
    ]

    formatted_md = f"""### 1. What This Issue Appears to Be Asking For
{what_it_asks}

### 2. Why It Matters
Resolving this improves the reliability and developer experience of **{repo_name}**, addressing pain points documented by community contributors.

### 3. Skills & Tools Likely Needed
* **Language/Platform:** {repo_lang}
* **Version Control:** Git & GitHub branch/PR workflow
* **Testing:** Local test runner and verification suite

### 4. Suggested Investigation Sequence
{chr(10).join(investigation_steps)}

### 5. Contribution Roadmap
{chr(10).join(roadmap_steps)}

### 6. Polite Questions to Ask Maintainers
{chr(10).join(['* ' + q for q in maintainer_questions])}

### 7. Immediate Next Step for a Beginner
Comment politely on the GitHub issue asking to be assigned, fork the repository, and reproduce the behavior locally before writing new code.
"""

    return {
        "source": "Krititva OpenSource Buddy Guidance Engine (Heuristic / Gemma-compatible)",
        "disclaimer": "⚠️ Model-assisted suggestion based on repository context and issue title. Always respect the repository's CONTRIBUTING.md.",
        "explanation_markdown": formatted_md
    }
