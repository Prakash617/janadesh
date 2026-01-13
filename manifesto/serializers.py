from rest_framework import serializers
from .models import Manifesto

class ManifestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manifesto
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "pdf_file",
            "status",
            "published_at",
            "created_at",
            "updated_at",
            "is_published",
        ]
        read_only_fields = ["created_at", "updated_at", "is_published"]
