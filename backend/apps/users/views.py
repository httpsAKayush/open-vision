from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer
from .services import build_user_profile


class AnalyzeUserView(APIView):
    """
    POST /api/users/analyze/
    Body: { "github_username": "torvalds" }
    """
    def post(self, request):
        username = request.data.get("github_username", "").strip()
        if not username:
            return Response(
                {"error": "github_username is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            profile_data = build_user_profile(username)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        profile, created = UserProfile.objects.update_or_create(
            github_username=username,
            defaults=profile_data
        )

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    GET /api/users/<username>/
    """
    def get(self, request, username):
        try:
            profile = UserProfile.objects.get(github_username=username)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "Profile not found. Run /analyze/ first."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)