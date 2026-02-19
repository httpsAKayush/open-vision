from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Issue
from .serializers import IssueSerializer
from .services import analyze_issues


class AnalyzeIssuesView(APIView):
    """
    POST /api/issues/analyze/
    Body: { "full_name": "opencv/opencv" }
    """
    def post(self, request):
        full_name = request.data.get("full_name", "").strip()
        if not full_name or "/" not in full_name:
            return Response(
                {"error": "full_name is required (e.g. 'opencv/opencv')"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            issues = analyze_issues(full_name)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        serializer = IssueSerializer(issues, many=True)
        return Response({
            "total": len(issues),
            "issues": serializer.data
        })


class IssueListView(APIView):
    """
    GET /api/issues/<owner>/<repo>/
    Optional query params: ?min_difficulty=1&max_difficulty=5
    """
    def get(self, request, owner, repo):
        full_name = f"{owner}/{repo}"
        qs = Issue.objects.filter(repository__github_full_name=full_name)

        min_d = request.query_params.get("min_difficulty")
        max_d = request.query_params.get("max_difficulty")
        if min_d:
            qs = qs.filter(difficulty_score__gte=float(min_d))
        if max_d:
            qs = qs.filter(difficulty_score__lte=float(max_d))

        qs = qs.order_by("difficulty_score")
        return Response(IssueSerializer(qs, many=True).data)