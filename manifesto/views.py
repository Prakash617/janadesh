from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Manifesto
from .serializers import ManifestoSerializer

class ManifestoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to list or retrieve manifestos
    """
    queryset = Manifesto.objects.filter(status="published")
    serializer_class = ManifestoSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
