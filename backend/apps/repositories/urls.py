from django.urls import path
from .views import AnalyzeRepoView, RepoDetailView

urlpatterns = [
    path("analyze/", AnalyzeRepoView.as_view(), name="analyze-repo"),
    path("<str:owner>/<str:repo>/", RepoDetailView.as_view(), name="repo-detail"),
]