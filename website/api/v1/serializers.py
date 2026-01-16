from rest_framework import serializers
from website.models import About, AboutImage, FutureVision,SocialMediaLink


class AboutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutImage
        fields = [
            "id",
            "image",
            "caption",
        ]


class AboutSerializer(serializers.ModelSerializer):
    images = AboutImageSerializer(many=True, read_only=True)

    class Meta:
        model = About
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "images",
            # "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
        

class FutureVisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureVision
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "image",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
        
class SocialMediaLinkSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(
        source="get_platform_display",
        read_only=True
    )

    class Meta:
        model = SocialMediaLink
        fields = [
            "id",
            "platform",
            "platform_display",
            "url",
            "icon",
            "order",
            "is_active",
        ]