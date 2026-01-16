from rest_framework import viewsets, permissions
from website.models import About
from .serializers import AboutSerializer


class AboutViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public About API (read-only)
    """
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [permissions.AllowAny]
