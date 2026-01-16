from rest_framework import serializers
from website.models import About, AboutImage


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
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
