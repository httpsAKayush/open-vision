from django.db import models


class UserProgress(models.Model):
    github_username = models.CharField(max_length=100)
    pr_url = models.URLField()
    pr_difficulty = models.FloatField()
    skill_before = models.FloatField()
    skill_after = models.FloatField()
    growth_factor = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.github_username}: {self.skill_before} → {self.skill_after}"