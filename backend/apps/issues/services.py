from .difficulty_engine import score_issue_difficulty


def enrich_issue(issue: dict) -> dict:
    issue['difficulty_score'] = score_issue_difficulty(issue)
    return issue
