from apps.users.models import UserProfile
from .matching_engine import match_issues_for_user, match_repos_for_user
from apps.issues.serializers import IssueSerializer
from apps.repositories.serializers import RepositorySerializer


def get_recommendations(username, full_name=None):
    try:
        user = UserProfile.objects.get(github_username=username)
    except UserProfile.DoesNotExist:
        raise ValueError(f"User '{username}' not found. Run /api/users/analyze/ first.")

    banded_issues = match_issues_for_user(user, full_name=full_name)

    return {
        "user": username,
        "skill_level": user.skill_level,
        "mode": "deep_dive" if full_name else "discovery",
        "recommendations": {
            "comfort": IssueSerializer(banded_issues.get("comfort", []), many=True).data,
            "growth": IssueSerializer(banded_issues.get("growth", []), many=True).data,
            "stretch": IssueSerializer(banded_issues.get("stretch", []), many=True).data,
        }
    }