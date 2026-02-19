from django.contrib import admin
from .models import UserProgress

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ["github_username", "skill_before", "skill_after", "growth_factor", "pr_difficulty", "created_at"]