from django.db import models


class Repository(models.Model):
    full_name = models.CharField(max_length=255, unique=True)
    complexity_score = models.FloatField(default=1)
    domain_embedding = models.JSONField(default=list)
    module_map = models.JSONField(default=dict)
