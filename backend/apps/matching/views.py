from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_recommendations
from .growth_engine import update_skill_from_pr


class RecommendView(APIView):
    """
    POST /api/matching/recommend/
    Body: { "github_username": "httpsAKayush" }
    Body (deep dive): { "github_username": "httpsAKayush", "full_name": "opencv/opencv" }
    """
    def post(self, request):
        username = request.data.get("github_username", "").strip()
        full_name = request.data.get("full_name", "").strip() or None

        if not username:
            return Response(
                {"error": "github_username is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            result = get_recommendations(username, full_name=full_name)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(result)


class GrowthUpdateView(APIView):
    """
    POST /api/matching/growth/
    Body: { "github_username": "httpsAKayush", "pr_url": "https://api.github.com/repos/..." }
    """
    def post(self, request):
        username = request.data.get("github_username", "").strip()
        pr_url = request.data.get("pr_url", "").strip()

        if not username or not pr_url:
            return Response(
                {"error": "github_username and pr_url are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            result = update_skill_from_pr(username, pr_url)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(result)