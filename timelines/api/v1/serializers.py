from rest_framework import serializers
from timelines.models import Timeline

class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = [
            'id', 'year', 'month', 'title_en', 'title_np',
            'description_en', 'description_np', 'image',
            'is_milestone', 'order', 'created_at', 'updated_at'
        ]
