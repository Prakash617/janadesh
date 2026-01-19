from rest_framework import serializers
from organization_app.models import Organization, Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address']


class OrganizationSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = [
            "id",
            "name_en",
            "name_np",
            "slug",
            "description_en",
            "description_np",
            "logo",
            "banner",
            "established_date",
            "email",
            "phone",
            "address_en",
            "address_np",
            "website",
            "facebook",
            "twitter",
            "instagram",
            "youtube",
            "created_at",
            "updated_at",
            "branches",
        ]
        read_only_fields = ("id", "created_at", "updated_at")
