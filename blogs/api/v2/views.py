from rest_framework.views import APIView
from rest_framework.response import Response

class BlogListAPIView(APIView):
    def get(self, request):
        return Response({
            "version": request.version,
            "app": "blogs",
            "status": "ok"
        })
