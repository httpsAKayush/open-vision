from .matching_engine import cosine_match


def recommend_repository(user_profile: dict, repositories: list[dict]) -> list[dict]:
    return sorted(repositories, key=lambda r: cosine_match(user_profile.get('domain_embedding', []), r.get('domain_embedding', [])), reverse=True)
