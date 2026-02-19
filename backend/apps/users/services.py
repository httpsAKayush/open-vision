import requests
from django.conf import settings
from collections import Counter
import math


GITHUB_API = "https://api.github.com"


def get_headers():
    return {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }


def fetch_repos(username):
    url = f"{GITHUB_API}/users/{username}/repos?per_page=100&sort=updated"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def fetch_pull_requests(username):
    url = f"{GITHUB_API}/search/issues?q=author:{username}+type:pr&per_page=100"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json().get("items", [])


def extract_languages(repos):
    lang_counter = Counter()
    for repo in repos:
        if repo.get("language"):
            lang_counter[repo["language"]] += 1
    return dict(lang_counter)


def extract_domain_keywords(repos):
    keywords = []
    for repo in repos:
        if repo.get("topics"):
            keywords.extend(repo["topics"])
        name = repo.get("name", "").replace("-", " ").replace("_", " ")
        keywords.extend(name.lower().split())
    # Return top 20 unique keywords
    counted = Counter(keywords)
    return [kw for kw, _ in counted.most_common(20)]


def compute_experience_score(repos, prs):
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)
    repo_count = len(repos)
    pr_count = len(prs)

    score = (
        math.log1p(total_stars) * 2 +
        math.log1p(total_forks) * 1.5 +
        math.log1p(repo_count) * 3 +
        math.log1p(pr_count) * 4
    )
    return round(score, 2)


def compute_skill_level(experience_score):
    # Normalize to 1–10 scale using a soft cap at score=100
    raw = (experience_score / 100) * 10
    return round(min(max(raw, 1.0), 10.0), 2)


def build_user_profile(username):
    repos = fetch_repos(username)
    prs = fetch_pull_requests(username)

    languages = extract_languages(repos)
    domain_keywords = extract_domain_keywords(repos)
    experience_score = compute_experience_score(repos, prs)
    skill_level = compute_skill_level(experience_score)

    return {
        "github_username": username,
        "experience_score": experience_score,
        "skill_level": skill_level,
        "domain_keywords": domain_keywords,
        "languages": languages,
        "total_repos": len(repos),
        "total_stars": sum(r.get("stargazers_count", 0) for r in repos),
        "total_prs": len(prs),
    }