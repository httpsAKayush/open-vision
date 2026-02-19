def cosine_match(user_embedding, repository_embedding) -> float:
    return 1.0 if user_embedding == repository_embedding else 0.5
