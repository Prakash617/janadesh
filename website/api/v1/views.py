from rest_framework import viewsets, permissions
from website.models import About,FutureVision,SocialMediaLink
from .serializers import AboutSerializer,FutureVisionSerializer,SocialMediaLinkSerializer


class AboutMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public About API (read-only)
    """
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [permissions.AllowAny]
    
class FutureVisionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public Future Vision API (active only)
    """
    queryset = FutureVision.objects.filter(is_active=True)
    serializer_class = FutureVisionSerializer
    permission_classes = [permissions.AllowAny]
    
class SocialMediaLinkViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public Social Media Links API
    """
    queryset = SocialMediaLink.objects.filter(is_active=True).order_by("order")
    serializer_class = SocialMediaLinkSerializer
    permission_classes = [permissions.AllowAny]
