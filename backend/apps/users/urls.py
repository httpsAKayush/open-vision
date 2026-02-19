from django.urls import path
from .views import AnalyzeUserView, UserProfileView

urlpatterns = [
    path("analyze/", AnalyzeUserView.as_view(), name="analyze-user"),
    path("<str:username>/", UserProfileView.as_view(), name="user-profile"),
]