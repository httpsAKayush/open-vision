from apps.users.models import UserProfile
from .matching_engine import match_issues_for_user, match_repos_for_user
from .module_anchoring import find_anchor_folders, anchor_issues_to_modules
from apps.issues.serializers import IssueSerializer
from apps.repositories.serializers import RepositorySerializer


def get_recommendations(username, full_name=None):
    try:
        user = UserProfile.objects.get(github_username=username)
    except UserProfile.DoesNotExist:
        raise ValueError(f"User '{username}' not found. Run /api/users/analyze/ first.")

    banded_issues = match_issues_for_user(user, full_name=full_name)

    # Serialize issues
    comfort = IssueSerializer(banded_issues.get("comfort", []), many=True).data
    growth = IssueSerializer(banded_issues.get("growth", []), many=True).data
    stretch = IssueSerializer(banded_issues.get("stretch", []), many=True).data

    # Anchor issues to modules using user keywords
    comfort = anchor_issues_to_modules(list(comfort), user.domain_keywords)
    growth = anchor_issues_to_modules(list(growth), user.domain_keywords)
    stretch = anchor_issues_to_modules(list(stretch), user.domain_keywords)

    # Find suggested entry folders in the repo
    anchor_folders = []
    if full_name:
        anchor_folders = find_anchor_folders(full_name, user.domain_keywords)

    return {
        "user": username,
        "skill_level": user.skill_level,
        "mode": "deep_dive" if full_name else "discovery",
        "anchor_folders": anchor_folders,
        "recommendations": {
            "comfort": comfort,
            "growth": growth,
            "stretch": stretch,
        }
    }