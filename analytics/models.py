from django.db import models

# Register your models here.

class AnalyticsEvent(models.Model):
    """Analytics event tracking"""
    EVENT_TYPE_CHOICES = [
        ('page_view', 'Page View'),
        ('blog_view', 'Blog View'),
        ('campaign_view', 'Campaign View'),
        ('download', 'Download'),
        ('form_submit', 'Form Submit'),
    ]
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    object_type = models.CharField(max_length=50, blank=True, null=True) #model name
    object_id = models.IntegerField(blank=True, null=True) #single model id
    url = models.TextField()
    referrer = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=5, default='en')
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analytics_events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['object_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"