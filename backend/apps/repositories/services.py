from .models import Repository
from .analyzers import analyze_repository


def get_or_analyze_repo(full_name):
    data = analyze_repository(full_name)
    repo, created = Repository.objects.update_or_create(
        github_full_name=full_name,
        defaults=data
    )
    return repo