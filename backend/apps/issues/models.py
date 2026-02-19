from django.db import models
from apps.repositories.models import Repository


class Issue(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='issues')
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    difficulty_score = models.FloatField(default=1)

    class Meta:
        unique_together = ('repository', 'number')
