from rest_framework import serializers
from services.models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "title_en",
            "title_np",
            "slug",
            "description_en",
            "description_np",
            "icon",
            "image",
            "is_active",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
