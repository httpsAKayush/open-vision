from django.db import models
from apps.repositories.models import Repository


class Issue(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="issues")
    github_issue_number = models.IntegerField()
    title = models.TextField()
    body = models.TextField(blank=True)
    labels = models.JSONField(default=list)
    comment_count = models.IntegerField(default=0)
    difficulty_score = models.FloatField(default=0.0)  # 1–10
    is_good_first_issue = models.BooleanField(default=False)
    is_bug = models.BooleanField(default=False)
    linked_pr_size = models.FloatField(default=0.0)
    resolution_time_days = models.FloatField(null=True, blank=True)
    html_url = models.URLField(blank=True)
    state = models.CharField(max_length=20, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("repository", "github_issue_number")

    def __str__(self):
        return f"#{self.github_issue_number} {self.title[:60]} (difficulty: {self.difficulty_score})"