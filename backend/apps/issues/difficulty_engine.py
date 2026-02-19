import re

TECHNICAL_KEYWORDS = [
    "segfault", "memory leak", "race condition", "deadlock", "overflow",
    "optimization", "refactor", "architecture", "kernel", "compiler",
    "algorithm", "complexity", "concurrency", "async", "multithread",
    "cuda", "gpu", "shader", "pipeline", "inference", "backprop",
    "gradient", "tensor", "vectorize", "simd", "intrinsic",
]

EASY_LABELS = {"good first issue", "good-first-issue", "beginner", "easy", "starter"}
MEDIUM_LABELS = {"help wanted", "enhancement", "feature"}
HARD_LABELS = {"bug", "critical", "performance", "security", "breaking change"}


def score_by_labels(labels):
    label_names = {l.lower() for l in labels}
    if label_names & EASY_LABELS:
        return 1.0
    if label_names & HARD_LABELS:
        return 3.0
    if label_names & MEDIUM_LABELS:
        return 2.0
    return 2.0  # default neutral


def score_by_keywords(title, body):
    text = (title + " " + body).lower()
    hits = sum(1 for kw in TECHNICAL_KEYWORDS if kw in text)
    return min(hits * 0.8, 4.0)


def score_by_comments(comment_count):
    # More comments = more discussion = more complex
    if comment_count == 0:
        return 0.0
    if comment_count <= 3:
        return 0.5
    if comment_count <= 10:
        return 1.0
    return 2.0


def score_by_body_length(body):
    length = len(body or "")
    if length < 100:
        return 0.0
    if length < 500:
        return 0.5
    if length < 1500:
        return 1.0
    return 1.5


def score_by_linked_pr_size(pr_size):
    if pr_size == 0:
        return 0.0
    if pr_size < 50:
        return 0.5
    if pr_size < 200:
        return 1.0
    if pr_size < 500:
        return 1.5
    return 2.0


def compute_difficulty_score(title, body, labels, comment_count, linked_pr_size):
    label_score = score_by_labels(labels)
    keyword_score = score_by_keywords(title, body)
    comment_score = score_by_comments(comment_count)
    body_score = score_by_body_length(body)
    pr_score = score_by_linked_pr_size(linked_pr_size)

    raw = label_score + keyword_score + comment_score + body_score + pr_score

    # Normalize to 1–10
    normalized = (raw / 12.5) * 10
    return round(min(max(normalized, 1.0), 10.0), 2)