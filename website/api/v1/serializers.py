from rest_framework import serializers
from website.models import About, AboutImage, FutureVision,SocialMediaLink,HeroSection, HeroNews


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
        source="platform.name",
        read_only=True
    )
    icon = serializers.CharField(
        source="platform.icon",
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
        
        
class HeroNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroNews
        fields = [
            "id",
            "description_en",
            "description_np",
            "created_at",
        ]

class HeroSectionSerializer(serializers.ModelSerializer):
    hero_news = HeroNewsSerializer(many=True, read_only=True)

    class Meta:
        model = HeroSection
        fields = [
            "id",

            # English
            "title_en",
            "subtitle_en",
            "description_en",
            "button_text_en",

            # Nepali
            "title_np",
            "subtitle_np",
            "description_np",
            "button_text_np",

            # Common
            "button_url",
            "main_image",
            "hero_news",
            "created_at",
            "updated_at",
        ]
