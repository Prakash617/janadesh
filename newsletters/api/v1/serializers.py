from rest_framework import serializers
from newsletters.models import NewsletterSubscription

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = [
            'id',
            'email',
            'name',
            'is_active',
            'subscribed_at',
            'unsubscribed_at',
        ]
        read_only_fields = [
            'id',
            'is_active',
            'subscribed_at',
            'unsubscribed_at',
        ]
