from django.db import models
import uuid
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError


from django.core.validators import MinValueValidator
from django.utils.text import slugify

User = get_user_model()


# Create your models here.
class Organization(models.Model):
    """Organization/Party profile"""

    name_en = models.CharField(max_length=255)
    name_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description_en = models.TextField()
    description_np = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="organization/organization/logo", null=True, blank=True
    )
    banner = models.ImageField(
        upload_to="organization/organization/banner", null=True, blank=True
    )
    established_date = models.DateField(blank=True, null=True)
    manifesto_en = models.TextField(blank=True, null=True)
    manifesto_np = models.TextField(blank=True, null=True)
    manifesto_document = models.FileField(
        upload_to="org_manifestos/", null=True, blank=True
    )
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
        db_table = "organizations"

    def __str__(self):
        return self.name_en


# ============================================================================
# MEMBERS MODULE
# ============================================================================
class Leadership(models.Model):
    """Organization members/leaders"""

    MEMBER_TYPE_CHOICES = [
        ("leader", "Leader"),
        ("member", "Member"),
        ("advisor", "Advisor"),
    ]

    name_en = models.CharField(max_length=255)
    name_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    position_en = models.CharField(max_length=255)
    position_np = models.CharField(max_length=255, blank=True, null=True)
    member_type = models.CharField(
        max_length=20, choices=MEMBER_TYPE_CHOICES, default="member"
    )
    bio_en = models.TextField(blank=True, null=True)
    bio_np = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="members/", null=True, blank=True)
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
        db_table = "members"
        ordering = ["order", "name_en"]

    def __str__(self):
        return f"{self.name_en} - {self.position_en}"


class MembershipRegistration(models.Model):
    """
    Membership registration applications with complete user details
    """

    MEMBERSHIP_TYPE_CHOICES = [
        ("member", "Member"),
        ("volunteer", "Volunteer"),
        ("donor", "Donor"),
    ]

    PROVINCE_CHOICES = [
        ("koshi", "Koshi"),
        ("madhesh", "Madhesh"),
        ("bagmati", "Bagmati"),
        ("gandaki", "Gandaki"),
        ("lumbini", "Lumbini"),
        ("karnali", "Karnali"),
        ("sudurpashchim", "Sudurpashchim"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    

    # Membership Information
    membership_type = models.CharField(
        max_length=20, choices=MEMBERSHIP_TYPE_CHOICES, verbose_name="Membership Type"
    )

    # Personal Information (व्यक्तिगत विवरण)
    full_name = models.CharField(
        max_length=100, verbose_name="Full Name", help_text="User's full name"
    )
    father_name = models.CharField(
        max_length=100, verbose_name="Father's Name", help_text="Father's full name"
    )
    mother_name = models.CharField(
        max_length=100, verbose_name="Mother's Name", help_text="Mother's full name"
    )
    date_of_birth = models.DateField(
        verbose_name="Date of Birth", help_text="Birth date in format MM/DD/YYYY"
    )
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, verbose_name="Gender"
    )
    phone_number = models.CharField(
        max_length=15, verbose_name="Phone Number", help_text="Contact phone number"
    )
    email = models.EmailField(
        verbose_name="Email Address", help_text="Contact email address"
    )

    # Location Details (ठेगाना विवरण)
    province = models.CharField(
        max_length=20, choices=PROVINCE_CHOICES, verbose_name="Province"
    )
    district = models.CharField(
        max_length=100, verbose_name="District", help_text="District name"
    )
    municipality = models.CharField(
        max_length=150,
        verbose_name="Municipality/Rural Municipality",
        help_text="Municipality or Rural Municipality name",
    )
    ward_number = models.CharField(
        max_length=10, verbose_name="Ward Number", help_text="Ward number"
    )
    village_settlement = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Village/Settlement",
        help_text="Village or Settlement name (optional)",
    )
    address = models.CharField(
        max_length=500, verbose_name="Full Address", help_text="Complete address"
    )

    # Document Information (कागजात अपलोड)
    citizenship_number = models.CharField(
        max_length=50,
        verbose_name="Citizenship Number",
        help_text="National citizenship ID number",
    )
    passport_photo = models.ImageField(
        upload_to="memberships/passport_photos/%Y/%m/",
        verbose_name="Passport Size Photo",
        help_text="Upload passport size photo (JPG, PNG or GIF, max 2MB)",
    )
    citizenship_copy = models.FileField(
        upload_to="memberships/citizenship_docs/%Y/%m/",
        verbose_name="Citizenship Copy",
        help_text="Upload citizenship document copy (PDF or Image, max 5MB)",
    )

    # Additional Information
    occupation = models.CharField(
        max_length=100,
        blank=True,null=True,
        verbose_name="Occupation",
        help_text="Current occupation or profession",
    )
    motivation = models.TextField(
        verbose_name="Motivation",
        help_text="Why do you want to join? What are your motivations?",blank=True,null=True
    )

    # Terms and Conditions
    terms_accepted = models.BooleanField(
        default=False,
        verbose_name="Terms Accepted",
        help_text="I accept the terms and conditions",
    )

    # Application Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Application Status",
    )
    approved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_memberships",
        verbose_name="Approved By",
    )
    approved_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Approval Date"
    )
    rejection_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name="Rejection Reason",
        help_text="Reason for rejection (if applicable)",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = "membership_registrations"
        verbose_name = "Membership Registration"
        verbose_name_plural = "Membership Registrations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["membership_type", "status"]),
            models.Index(fields=["province", "district"]),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.membership_type} ({self.status})"

    # def get_full_name(self):
    #     """Return full name"""
    #     return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            if age < 18:
                raise ValidationError({
                    'date_of_birth': 'You must be at least 18 years old to register.'
                })
                
    def get_full_address(self):
        """Return formatted full address"""
        parts = [
            self.village_settlement,
            f"Ward {self.ward_number}",
            self.municipality,
            self.district,
            self.get_province_display(),
        ]
        return ", ".join(filter(None, parts))

    def approve(self, approved_by_user):
        """Approve the membership application"""
        from django.utils import timezone

        self.status = "approved"
        self.approved_by = approved_by_user
        self.approved_at = timezone.now()
        self.save()

    def reject(self, reason=None):
        """Reject the membership application"""
        self.status = "rejected"
        if reason:
            self.rejection_reason = reason
        self.save()

    @property
    def is_pending(self):
        return self.status == "pending"

    @property
    def is_approved(self):
        return self.status == "approved"

    @property
    def is_rejected(self):
        return self.status == "rejected"
    
    def save(self, *args, **kwargs):
        self.full_clean()  # ensures clean() is called on save
        super().save(*args, **kwargs)

    
class PolicyCategory(models.Model):
    """Policy Categories"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_en = models.CharField(max_length=100, unique=True)
    name_ne = models.CharField(
        max_length=100, blank=True, verbose_name="Name (Nepali)"
    )
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    icon = models.CharField(
        max_length=100, blank=True, help_text="Icon class or image path"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "policy_categories"
        verbose_name = "Policy Category"
        verbose_name_plural = "Policy Categories"
        ordering = ["order", "name_en"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_en


class Policy(models.Model):
    """Policies and Initiatives"""

    CATEGORY_CHOICES = [
        ("governance", "Transparent Governance"),
        ("economy", "Sustainable Economy"),
        ("environment", "Environment/Infrastructure"),
        ("society", "Inclusive Society"),
        ("digital", "Digital Governance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    title_ne = models.CharField(
        max_length=255, blank=True, verbose_name="Title (Nepali)"
    )
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField()
    description_ne = models.TextField(blank=True, verbose_name="Description (Nepali)")
    icon = models.CharField(
        max_length=100, blank=True, help_text="Icon identifier or path"
    )
    # category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    category = models.ForeignKey(
        PolicyCategory,
        on_delete=models.PROTECT,
        related_name="policies", blank=True, null=True
    )
    content = models.TextField(blank=True, help_text="Detailed policy content")
    content_ne = models.TextField(blank=True, verbose_name="Content (Nepali)")
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "policies"
        verbose_name = "Policy"
        verbose_name_plural = "Policies"
        ordering = ["order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Donation(models.Model):
    """Donations tracking"""

    PAYMENT_METHOD_CHOICES = [
        ("esewa", "eSewa"),
        ("khalti", "Khalti"),
        ("bank_transfer", "Bank Transfer"),
        ("cash", "Cash"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        # ('refunded', 'Refunded'a),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations",
    )
    donor_name = models.CharField(max_length=255)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=15, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=10, default="NPR")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    message = models.TextField(blank=True, help_text="Optional donor message")
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "donations"
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.donor_name} - {self.amount} {self.currency}"
