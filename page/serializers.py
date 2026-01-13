from rest_framework import serializers
from .models import Page

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            "id",
            "title",
            "slug",
            "meta_description",
            "content",
            "excerpt",
            "featured_image",
            "seo_title",
            "keywords",
            "status",
            "published_at",
            "created_at",
            "updated_at",
            "is_published",
        ]
        read_only_fields = ["created_at", "updated_at", "is_published"]
