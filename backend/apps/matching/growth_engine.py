from apps.users.models import UserProfile
import requests
from django.conf import settings
import math


GITHUB_API = "https://api.github.com"


def get_headers():
    return {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }


def estimate_pr_difficulty(pr_url):
    r = requests.get(pr_url, headers=get_headers())
    if r.status_code != 200:
        return 1.0
    pr = r.json()
    additions = pr.get("additions", 0)
    deletions = pr.get("deletions", 0)
    changed_files = pr.get("changed_files", 0)
    size = additions + deletions

    if size < 50:
        return 1.0
    if size < 200:
        return 2.0
    if size < 500:
        return 3.0
    return 4.0


def compute_growth_factor(pr_difficulty, current_skill):
    # Larger gain when PR is harder than current skill
    delta = pr_difficulty - current_skill
    if delta <= 0:
        return 0.05   # small gain for easy PRs
    return round(min(delta * 0.1, 0.5), 3)


def update_skill_from_pr(username, pr_url):
    try:
        profile = UserProfile.objects.get(github_username=username)
    except UserProfile.DoesNotExist:
        raise ValueError(f"User '{username}' not found.")

    pr_difficulty = estimate_pr_difficulty(pr_url)
    growth = compute_growth_factor(pr_difficulty, profile.skill_level)

    old_skill = profile.skill_level
    new_skill = round(min(old_skill + growth, 10.0), 3)

    profile.skill_level = new_skill
    profile.save()

    return {
        "github_username": username,
        "old_skill": old_skill,
        "pr_difficulty": pr_difficulty,
        "growth_factor": growth,
        "new_skill": new_skill,
    }