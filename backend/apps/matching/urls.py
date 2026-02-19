from django.urls import path
from .views import RecommendView, GrowthUpdateView

urlpatterns = [
    path("recommend/", RecommendView.as_view(), name="recommend"),
    path("growth/", GrowthUpdateView.as_view(), name="growth-update"),
]