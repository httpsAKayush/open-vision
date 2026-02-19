from django.urls import path
from .views import AnalyzeIssuesView, IssueListView

urlpatterns = [
    path("analyze/", AnalyzeIssuesView.as_view(), name="analyze-issues"),
    path("<str:owner>/<str:repo>/", IssueListView.as_view(), name="issue-list"),
]