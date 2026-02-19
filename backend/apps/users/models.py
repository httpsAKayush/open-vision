from django.db import models


class UserProfile(models.Model):
    github_username = models.CharField(max_length=255, unique=True)
    skill_level = models.IntegerField(default=1)
    experience_score = models.FloatField(default=0)
    complexity_tolerance = models.FloatField(default=1)
    domain_embedding = models.JSONField(default=list)
