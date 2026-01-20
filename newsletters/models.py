from django.db import models
import uuid

# Create your models here.
class NewsletterSubscription(models.Model):
    """Newsletter email subscriptions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'newsletter_subscriptions'
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscription'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email