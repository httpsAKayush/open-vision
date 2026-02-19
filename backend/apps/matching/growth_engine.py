def update_skill(current_skill: float, handled_difficulty: float) -> float:
    return min(10.0, current_skill + (handled_difficulty / 20.0))
