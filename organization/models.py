from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify

# Create your models here.
class Organization(models.Model):
    """Organization/Party profile"""
    name_en = models.CharField(max_length=255)
    name_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description_en = models.TextField()
    description_np = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='organization/organization/logo', null=True, blank=True)
    banner = models.ImageField(upload_to='organization/organization/banner', null=True, blank=True)
    established_date = models.DateField(blank=True, null=True)
    manifesto_en = models.TextField(blank=True, null=True)
    manifesto_np = models.TextField(blank=True, null=True)
    manifesto_document = models.FileField(upload_to='org_manifestos/', null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_en = models.TextField(blank=True, null=True)
    address_np = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'organizations'

    def __str__(self):
        return self.name_en


# ============================================================================
# MEMBERS MODULE
# ============================================================================
class Leadership(models.Model):
    """Organization members/leaders"""
    MEMBER_TYPE_CHOICES = [
        ('leader', 'Leader'),
        ('member', 'Member'),
        ('advisor', 'Advisor'),
    ]
    
    name_en = models.CharField(max_length=255)
    name_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    position_en = models.CharField(max_length=255)
    position_np = models.CharField(max_length=255, blank=True, null=True)
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES, default='member')
    bio_en = models.TextField(blank=True, null=True)
    bio_np = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='members/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'members'
        ordering = ['order', 'name_en']

    def __str__(self):
        return f"{self.name_en} - {self.position_en}"
    
    

class MembershipRegistration(models.Model):
    """Membership registration applications"""
    MEMBERSHIP_TYPE_CHOICES = [
        ('member', 'Member'),
        ('volunteer', 'Volunteer'),
        ('donor', 'Donor'),
    ]
    
    PROVINCE_CHOICES = [
        ('koshi', 'Koshi'),
        ('gandaki', 'Gandaki'),
        ('madhesh', 'Madhesh'),
        ('bagmati', 'Bagmati'),
        ('lumbini', 'Lumbini'),
        ('sudurpashchim', 'Sudurpashchim'),
        ('karnali', 'Karnali'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPE_CHOICES)
    province = models.CharField(max_length=20, choices=PROVINCE_CHOICES)
    address = models.CharField(max_length=500)
    citizenship_number = models.CharField(max_length=50, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    motivation = models.TextField(help_text='Why do you want to join?')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_memberships')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'membership_registrations'
        verbose_name = 'Membership Registration'
        verbose_name_plural = 'Membership Registrations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.membership_type} ({self.status})"

class Policy(models.Model):
    """Policies and Initiatives"""
    CATEGORY_CHOICES = [
        ('governance', 'Transparent Governance'),
        ('economy', 'Sustainable Economy'),
        ('environment', 'Environment/Infrastructure'),
        ('society', 'Inclusive Society'),
        ('digital', 'Digital Governance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    title_ne = models.CharField(max_length=255, blank=True, verbose_name='Title (Nepali)')
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField()
    description_ne = models.TextField(blank=True, verbose_name='Description (Nepali)')
    icon = models.CharField(max_length=100, blank=True, help_text='Icon identifier or path')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField(blank=True, help_text='Detailed policy content')
    content_ne = models.TextField(blank=True, verbose_name='Content (Nepali)')
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'policies'
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'
        ordering = ['order', 'title']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Donation(models.Model):
    """Donations tracking"""
    PAYMENT_METHOD_CHOICES = [
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        # ('refunded', 'Refunded'a),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    donor_name = models.CharField(max_length=255)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=15, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default='NPR')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text='Optional donor message')
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'donations'
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.donor_name} - {self.amount} {self.currency}"
