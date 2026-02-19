from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["github_username", "skill_level", "experience_score", "total_repos", "total_prs"]