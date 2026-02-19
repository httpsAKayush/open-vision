from django.contrib import admin
from .models import Issue

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["github_issue_number", "title", "difficulty_score", "is_good_first_issue", "comment_count"]
    list_filter = ["is_good_first_issue", "is_bug"]