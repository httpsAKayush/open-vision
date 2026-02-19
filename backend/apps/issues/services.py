import requests
from django.conf import settings
from .models import Issue
from .difficulty_engine import compute_difficulty_score
from apps.repositories.models import Repository


GITHUB_API = "https://api.github.com"


def get_headers():
    return {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }


def fetch_issues(full_name, state="open", per_page=50):
    url = f"{GITHUB_API}/repos/{full_name}/issues?state={state}&per_page={per_page}&sort=updated"
    r = requests.get(url, headers=get_headers())
    r.raise_for_status()
    # Filter out pull requests (GitHub returns them mixed with issues)
    return [i for i in r.json() if "pull_request" not in i]


def analyze_issues(full_name):
    try:
        repo = Repository.objects.get(github_full_name=full_name)
    except Repository.DoesNotExist:
        raise ValueError(f"Repository '{full_name}' not found. Analyze it first via /api/repositories/analyze/")

    raw_issues = fetch_issues(full_name)
    saved = []

    for raw in raw_issues:
        labels = [l["name"] for l in raw.get("labels", [])]
        title = raw.get("title", "")
        body = raw.get("body", "") or ""
        comment_count = raw.get("comments", 0)
        is_good_first = any(
            l.lower() in {"good first issue", "good-first-issue"} for l in labels
        )
        is_bug = any("bug" in l.lower() for l in labels)

        difficulty = compute_difficulty_score(
            title=title,
            body=body,
            labels=labels,
            comment_count=comment_count,
            linked_pr_size=0.0,
        )

        issue, _ = Issue.objects.update_or_create(
            repository=repo,
            github_issue_number=raw["number"],
            defaults={
                "title": title,
                "body": body[:5000],
                "labels": labels,
                "comment_count": comment_count,
                "difficulty_score": difficulty,
                "is_good_first_issue": is_good_first,
                "is_bug": is_bug,
                "html_url": raw.get("html_url", ""),
                "state": raw.get("state", "open"),
            }
        )
        saved.append(issue)

    return saved