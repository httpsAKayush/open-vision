def score_issue_difficulty(issue: dict) -> float:
    labels = issue.get('labels', [])
    if 'good-first-issue' in labels:
        return 2.0
    return 5.0
