from rest_framework import serializers
from campaign.models import Campaign, CampaignActivity, Volunteer


# -------------------------------
# CampaignActivity Serializer
# -------------------------------
class CampaignActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignActivity
        fields = [
            "id",
            "campaign",
            "title_en",
            "title_np",
            "description_en",
            "description_np",
            "activity_type",
            "location_en",
            "location_np",
            "date",
            "start_time",
            "end_time",
            "participants_count",
            "image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


# -------------------------------
# Volunteer Serializer
# -------------------------------
class VolunteerSerializer(serializers.ModelSerializer):
    campaign_info = serializers.SerializerMethodField()
    campaign_slug = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Campaign.objects.all(),
        source="campaign",
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Volunteer
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address",
            'membership_type',
            'campaign_slug',
            "campaign_info",
            "skills",
            "availability",
            # "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_campaign_info(self, obj):
        if obj.campaign:
            return {
                "slug": obj.campaign.slug,
                "title": obj.campaign.title_en
            }
        return None

# -------------------------------
# Campaign Serializer
# -------------------------------
class CampaignSerializer(serializers.ModelSerializer):
    # Nested relationships
    activities = CampaignActivitySerializer(many=True, read_only=True)
    volunteers = VolunteerSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = [
            "id",
            "title_en",
            "title_np",
            "slug",
            "description_en",
            "description_np",
            "banner",
            "start_date",
            "end_date",
            "region_en",
            "region_np",
            "status",
            "goal",
            "is_featured",
            "created_by",
            "created_at",
            "updated_at",
            "activities",
            "volunteers",
        ]
        read_only_fields = ["created_at", "updated_at"]
