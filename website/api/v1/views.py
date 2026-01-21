from rest_framework import viewsets, permissions
from website.models import About,FutureVision,SocialMediaLink,HeroSection
from .serializers import AboutSerializer,FutureVisionSerializer,SocialMediaLinkSerializer,HeroSectionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HeroSectionViewSet(viewsets.ViewSet):
    """
    Returns the singleton HeroSection with its HeroNews
    """

    def list(self, request):
        hero_section = (
            HeroSection.objects
            .prefetch_related("hero_news")
            .first()
        )

        if not hero_section:
            return Response(
                {"detail": "Hero section not configured"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = HeroSectionSerializer(hero_section)
        return Response(serializer.data, status=status.HTTP_200_OK)