# serializers.py
from rest_framework import serializers
from analytics.models import AnalyticsEvent


class AnalyticsEventSerializer(serializers.ModelSerializer):
    """Serializer for AnalyticsEvent"""
    
    class Meta:
        model = AnalyticsEvent
        fields = [
            'id',
            'event_type',
            'object_type',
            'object_id',
            'url',
            'referrer',
            'ip_address',
            'user_agent',
            'session_id',
            'language',
            'country',
            'city',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class AnalyticsEventCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating analytics events"""
    
    class Meta:
        model = AnalyticsEvent
        fields = [
            'event_type',
            'object_type',
            'object_id',
            'url',
            'referrer',
            'ip_address',
            'user_agent',
            'session_id',
            'language',
            'country',
            'city',
        ]
    
    def validate_event_type(self, value):
        """Validate event type"""
        valid_types = [choice[0] for choice in AnalyticsEvent.EVENT_TYPE_CHOICES]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid event type. Must be one of: {', '.join(valid_types)}"
            )
        return value


class AnalyticsEventListSerializer(serializers.ModelSerializer):
    """Simple serializer for listing analytics events"""
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    
    class Meta:
        model = AnalyticsEvent
        fields = [
            'id',
            'event_type',
            'event_type_display',
            'object_type',
            'object_id',
            'url',
            'ip_address',
            'language',
            'country',
            'city',
            'created_at',
        ]


class AnalyticsStatsSerializer(serializers.Serializer):
    """Serializer for analytics statistics"""
    total_events = serializers.IntegerField()
    total_page_views = serializers.IntegerField()
    total_blog_views = serializers.IntegerField()
    total_campaign_views = serializers.IntegerField()
    total_downloads = serializers.IntegerField()
    total_form_submits = serializers.IntegerField()
    unique_sessions = serializers.IntegerField()
    unique_ips = serializers.IntegerField()
    top_pages = serializers.ListField()
    top_countries = serializers.ListField()
    events_by_date = serializers.ListField()

