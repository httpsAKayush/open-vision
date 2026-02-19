import requests
from django.conf import settings
from apps.users.models import UserProfile
from apps.repositories.models import Repository


GITHUB_API = "https://api.github.com"


def get_headers():
    return {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }


def fetch_tree(full_name):
    url = f"{GITHUB_API}/repos/{full_name}/git/trees/HEAD?recursive=1"
    r = requests.get(url, headers=get_headers())
    if r.status_code != 200:
        return []
    return r.json().get("tree", [])


def extract_folders(tree):
    folders = set()
    for item in tree:
        path = item.get("path", "")
        parts = path.split("/")
        # Only take top 2 levels of folders
        if item.get("type") == "tree" and len(parts) <= 2:
            folders.add(path)
    return list(folders)


def score_folder(folder_path, user_keywords):
    folder_lower = folder_path.lower().replace("/", " ").replace("-", " ").replace("_", " ")
    folder_words = set(folder_lower.split())
    user_set = set(kw.lower() for kw in user_keywords)
    overlap = folder_words & user_set
    return len(overlap)


def find_anchor_folders(full_name, user_keywords, top_n=3):
    if not user_keywords:
        return []

    tree = fetch_tree(full_name)
    folders = extract_folders(tree)

    if not folders:
        return []

    scored = []
    for folder in folders:
        score = score_folder(folder, user_keywords)
        if score > 0:
            scored.append((folder, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [f"/{folder}" for folder, _ in scored[:top_n]]


def anchor_issues_to_modules(issues, user_keywords):
    """
    For each issue, find which module/folder it likely belongs to
    based on keyword matching against the issue title and body.
    """
    anchored = []
    for issue in issues:
        text = (issue.get("title", "") + " " + issue.get("body", "")).lower()
        matched_keywords = [
            kw for kw in user_keywords if kw.lower() in text
        ]
        issue["matched_keywords"] = matched_keywords
        anchored.append(issue)
    return anchored