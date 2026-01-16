from rest_framework import viewsets
from campaign.models import Campaign, CampaignActivity, Volunteer
from .serializers import CampaignSerializer, CampaignActivitySerializer, VolunteerSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


# Campaigns
class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    lookup_field = 'slug'  # optional: use slug instead of id
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]    # order 

# Activities
class CampaignActivityViewSet(viewsets.ModelViewSet):
    queryset = CampaignActivity.objects.all()
    serializer_class = CampaignActivitySerializer

# Volunteers
class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.AllowAny]
