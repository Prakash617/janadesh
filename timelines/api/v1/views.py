from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from janadesh.filters import LimitFilter  # your custom limit backend
from timelines.models import Timeline
from .serializers import TimelineSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class TimelineViewSet(viewsets.ModelViewSet):
    """
    API endpoint for timeline entries.
    """
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    permission_classes = [permissions.AllowAny]  # change to IsAdminUser if needed

    # -----------------------------
    # Filters & ordering
    # -----------------------------
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, LimitFilter]
    filterset_fields = ['year', 'month', 'is_milestone']  # filterable fields
    ordering_fields = ['year', 'month', 'order', 'created_at']
    ordering = ['-year', '-month', 'order']  # default ordering

    # -----------------------------
    # Featured/milestone endpoint
    # -----------------------------
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny], url_path='milestones')
    def milestones(self, request):
        """
        Returns only timeline entries marked as milestones
        """
        milestones = Timeline.objects.filter(is_milestone=True)
        milestones = self.filter_queryset(milestones)  # apply limit & filters
        serializer = self.get_serializer(milestones, many=True)
        return Response(serializer.data)
