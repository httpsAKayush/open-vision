from apps.users.models import UserProfile
from apps.repositories.models import Repository
from apps.issues.models import Issue
from collections import Counter


def keyword_similarity(user_keywords, repo_topics, repo_name, repo_description):
    if not user_keywords:
        return 0.0

    repo_text = set(
        repo_topics +
        repo_name.lower().replace("-", " ").replace("_", " ").split() +
        (repo_description or "").lower().split()
    )

    user_set = set(kw.lower() for kw in user_keywords)
    overlap = user_set & repo_text
    similarity = len(overlap) / len(user_set)
    return round(similarity, 4)


def get_difficulty_band(skill_level):
    return {
        "comfort": (max(1.0, skill_level - 1), skill_level),
        "growth": (skill_level, skill_level + 1),
        "stretch": (skill_level + 1, skill_level + 2),
    }


def filter_issues_by_band(issues, skill_level):
    band = get_difficulty_band(skill_level)
    result = {"comfort": [], "growth": [], "stretch": []}

    for issue in issues:
        d = issue.difficulty_score
        if band["comfort"][0] <= d <= band["comfort"][1]:
            result["comfort"].append(issue)
        elif band["growth"][0] < d <= band["growth"][1]:
            result["growth"].append(issue)
        elif band["stretch"][0] < d <= band["stretch"][1]:
            result["stretch"].append(issue)

    return result


def match_repos_for_user(user: UserProfile, top_n=5):
    repos = Repository.objects.all()
    scored = []

    for repo in repos:
        # Filter out repos too complex for the user
        if repo.complexity_score > user.skill_level + 2:
            continue

        similarity = keyword_similarity(
            user.domain_keywords,
            repo.topics,
            repo.name,
            repo.description,
        )

        # Growth bias: slightly prefer repos just above user level
        growth_bias = 0.1 if repo.complexity_score > user.skill_level else 0.0

        final_score = similarity + growth_bias
        scored.append((repo, final_score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [repo for repo, _ in scored[:top_n]]


def match_issues_for_user(user: UserProfile, full_name=None):
    if full_name:
        issues = Issue.objects.filter(
            repository__github_full_name=full_name,
            state="open"
        )
    else:
        repos = match_repos_for_user(user, top_n=3)
        if not repos:
            return {}
        issues = Issue.objects.filter(repository__in=repos, state="open")

    banded = filter_issues_by_band(list(issues), user.skill_level)
    return banded