import requests
import math
from django.conf import settings


GITHUB_API = "https://api.github.com"


def get_headers():
    return {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }


def fetch_repo_metadata(full_name):
    url = f"{GITHUB_API}/repos/{full_name}"
    r = requests.get(url, headers=get_headers())
    r.raise_for_status()
    return r.json()


def fetch_contributors(full_name):
    url = f"{GITHUB_API}/repos/{full_name}/contributors?per_page=100"
    r = requests.get(url, headers=get_headers())
    if r.status_code == 204:
        return []
    r.raise_for_status()
    return r.json()


def fetch_recent_prs(full_name):
    url = f"{GITHUB_API}/repos/{full_name}/pulls?state=closed&per_page=30"
    r = requests.get(url, headers=get_headers())
    r.raise_for_status()
    return r.json()


def fetch_languages(full_name):
    url = f"{GITHUB_API}/repos/{full_name}/languages"
    r = requests.get(url, headers=get_headers())
    r.raise_for_status()
    return r.json()


def fetch_tree(full_name):
    # Get file tree to estimate module depth
    url = f"{GITHUB_API}/repos/{full_name}/git/trees/HEAD?recursive=1"
    r = requests.get(url, headers=get_headers())
    if r.status_code != 200:
        return []
    data = r.json()
    return data.get("tree", [])


def compute_module_depth(tree):
    max_depth = 0
    for item in tree:
        depth = item.get("path", "").count("/")
        if depth > max_depth:
            max_depth = depth
    return max_depth


def compute_activity_score(repo_meta):
    # Based on stars, forks, open issues, watchers
    stars = repo_meta.get("stargazers_count", 0)
    forks = repo_meta.get("forks_count", 0)
    watchers = repo_meta.get("watchers_count", 0)
    issues = repo_meta.get("open_issues_count", 0)

    score = (
        math.log1p(stars) * 2 +
        math.log1p(forks) * 2 +
        math.log1p(watchers) +
        math.log1p(issues)
    )
    return round(score, 2)


def compute_average_pr_size(prs):
    if not prs:
        return 0.0
    sizes = []
    for pr in prs:
        additions = pr.get("additions", 0)
        deletions = pr.get("deletions", 0)
        sizes.append(additions + deletions)
    return round(sum(sizes) / len(sizes), 2) if sizes else 0.0


def compute_complexity_score(contributor_count, module_depth, avg_pr_size, activity_score, language_count):
    raw = (
        math.log1p(contributor_count) * 2 +
        module_depth * 0.5 +
        math.log1p(avg_pr_size) * 1.5 +
        activity_score * 0.3 +
        language_count * 0.5
    )
    # Normalize to 1–10
    normalized = (raw / 40) * 10
    return round(min(max(normalized, 1.0), 10.0), 2)


def analyze_repository(full_name):
    meta = fetch_repo_metadata(full_name)
    contributors = fetch_contributors(full_name)
    prs = fetch_recent_prs(full_name)
    languages = fetch_languages(full_name)
    tree = fetch_tree(full_name)

    contributor_count = len(contributors)
    module_depth = compute_module_depth(tree)
    avg_pr_size = compute_average_pr_size(prs)
    activity_score = compute_activity_score(meta)
    complexity_score = compute_complexity_score(
        contributor_count, module_depth, avg_pr_size,
        activity_score, len(languages)
    )

    return {
        "github_full_name": full_name,
        "name": meta.get("name", ""),
        "description": meta.get("description", "") or "",
        "complexity_score": complexity_score,
        "language_distribution": languages,
        "module_depth": module_depth,
        "contributor_count": contributor_count,
        "average_pr_size": avg_pr_size,
        "activity_score": activity_score,
        "stars": meta.get("stargazers_count", 0),
        "forks": meta.get("forks_count", 0),
        "open_issues_count": meta.get("open_issues_count", 0),
        "topics": meta.get("topics", []),
        "primary_language": meta.get("language", "") or "",
    }