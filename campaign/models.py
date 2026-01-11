from django.db import models
from django.conf import settings

# Create your models here.
class Campaign(models.Model):
    """Campaign management"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title_en = models.CharField(max_length=255)
    title_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description_en = models.TextField()
    description_np = models.TextField(blank=True, null=True)
    banner = models.ImageField(upload_to='campaign/campaign/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    region_en = models.CharField(max_length=255, blank=True, null=True)
    region_np = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    goal = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'campaigns'
        ordering = ['-start_date']

    def __str__(self):
        return self.title_en


class CampaignActivity(models.Model):
    """Campaign activities/events"""
    ACTIVITY_TYPE_CHOICES = [
        ('rally', 'Rally'),
        ('event', 'Event'),
        ('door_to_door', 'Door to Door'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='activities')
    title_en = models.CharField(max_length=255)
    title_np = models.CharField(max_length=255, blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    description_np = models.TextField(blank=True, null=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    location_en = models.CharField(max_length=255)
    location_np = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True,help_text="Enter the start time of the event (HH:MM or HH:MM:SS).")
    end_time = models.TimeField(blank=True, null=True,help_text="Enter the end time of the event (HH:MM or HH:MM:SS).")
    participants_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='campaign/campaign_activity/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'campaign_activities'
        ordering = ['-date']
        verbose_name_plural = 'Campaign Activities'

    def __str__(self):
        return f"{self.campaign.title_en} - {self.title_en}"


class Volunteer(models.Model):
    """Volunteer management"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='volunteers')
    skills = models.TextField(blank=True, null=True)
    availability = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'volunteers'
        ordering = ['-created_at']

    def __str__(self):
        return self.name