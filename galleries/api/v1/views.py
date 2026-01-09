from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from janadesh.filters import LimitFilter  # your custom limit filter
from galleries.models import Gallery
from .serializers import GallerySerializer

class GalleryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for gallery albums and images.
    """
    queryset = Gallery.objects.prefetch_related('images').all()
    serializer_class = GallerySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, LimitFilter]
    filterset_fields = ['is_featured']  # filter by featured albums

    # Default ordering: order -> created_at (from model Meta)
    ordering_fields = ['order', 'created_at']

    # ----------------------------
    # Featured galleries
    # ----------------------------
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny], url_path='featured')
    def featured(self, request):
        featured_galleries = Gallery.objects.filter(is_featured=True)
        featured_galleries = self.filter_queryset(featured_galleries)  # apply limit & filters
        serializer = self.get_serializer(featured_galleries, many=True)
        return Response(serializer.data)
