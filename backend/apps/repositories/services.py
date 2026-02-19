def compute_repository_complexity(data: dict) -> float:
    return float(data.get('complexity_score', 1))
