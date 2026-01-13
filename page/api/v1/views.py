from rest_framework import viewsets, permissions
from page.models import Page
from .serializers import PageSerializer

class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to list pages or retrieve a single page.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [permissions.AllowAny]  # public API
    lookup_field = "slug"  # access page by slug in URL

    # Optional: filter only published pages
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status="published")
