from rest_framework import serializers
from contacts.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ["status", "ip_address", "user_agent", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request:
            validated_data["ip_address"] = request.META.get("REMOTE_ADDR")
            validated_data["user_agent"] = request.META.get("HTTP_USER_AGENT")
        return super().create(validated_data)
