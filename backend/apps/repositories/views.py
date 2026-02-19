from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Repository
from .serializers import RepositorySerializer
from .services import get_or_analyze_repo


class AnalyzeRepoView(APIView):
    """
    POST /api/repositories/analyze/
    Body: { "full_name": "microsoft/vscode" }
    """
    def post(self, request):
        full_name = request.data.get("full_name", "").strip()
        if not full_name or "/" not in full_name:
            return Response(
                {"error": "full_name is required (e.g. 'microsoft/vscode')"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            repo = get_or_analyze_repo(full_name)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(RepositorySerializer(repo).data)


class RepoDetailView(APIView):
    """
    GET /api/repositories/<owner>/<repo>/
    """
    def get(self, request, owner, repo):
        full_name = f"{owner}/{repo}"
        try:
            repository = Repository.objects.get(github_full_name=full_name)
        except Repository.DoesNotExist:
            return Response(
                {"error": "Not found. Run /analyze/ first."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(RepositorySerializer(repository).data)