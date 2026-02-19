from django.db import models


class UserProfile(models.Model):
    github_username = models.CharField(max_length=100, unique=True)
    experience_score = models.FloatField(default=0.0)
    skill_level = models.FloatField(default=1.0)  # 1–10
    domain_keywords = models.JSONField(default=list)
    languages = models.JSONField(default=dict)
    total_repos = models.IntegerField(default=0)
    total_stars = models.IntegerField(default=0)
    total_prs = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.github_username} (skill: {self.skill_level})"