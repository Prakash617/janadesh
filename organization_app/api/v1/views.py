from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from organization_app.models import Organization
from .serializers import OrganizationSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.prefetch_related('branches').all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can access
