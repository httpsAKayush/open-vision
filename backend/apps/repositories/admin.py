from django.contrib import admin
from .models import Repository

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ["github_full_name", "complexity_score", "contributor_count", "stars", "primary_language"]