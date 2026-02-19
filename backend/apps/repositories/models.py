from django.db import models


class Repository(models.Model):
    github_full_name = models.CharField(max_length=200, unique=True)  # e.g. "torvalds/linux"
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    complexity_score = models.FloatField(default=0.0)  # 1–10
    language_distribution = models.JSONField(default=dict)
    module_depth = models.IntegerField(default=0)
    contributor_count = models.IntegerField(default=0)
    average_pr_size = models.FloatField(default=0.0)
    activity_score = models.FloatField(default=0.0)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    open_issues_count = models.IntegerField(default=0)
    topics = models.JSONField(default=list)
    primary_language = models.CharField(max_length=100, blank=True)
    last_analyzed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.github_full_name} (complexity: {self.complexity_score})"