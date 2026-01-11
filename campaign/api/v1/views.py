from rest_framework import viewsets
from campaign.models import Campaign, CampaignActivity, Volunteer
from .serializers import CampaignSerializer, CampaignActivitySerializer, VolunteerSerializer

# Campaigns
class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    lookup_field = 'slug'  # optional: use slug instead of id
    # order 

# Activities
class CampaignActivityViewSet(viewsets.ModelViewSet):
    queryset = CampaignActivity.objects.all()
    serializer_class = CampaignActivitySerializer

# Volunteers
class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
