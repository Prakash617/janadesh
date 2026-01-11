import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    PROVINCE_CHOICES = [
        ('koshi', 'Koshi'),
        ('gandaki', 'Gandaki'),
        ('madhesh', 'Madhesh'),
        ('bagmati', 'Bagmati'),
        ('lumbini', 'Lumbini'),
        ('sudurpashchim', 'Sudurpashchim'),
        ('karnali', 'Karnali'),
    ]

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('volunteer', 'Volunteer'),
        ('donor', 'Donor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    province = models.CharField(max_length=20, choices=PROVINCE_CHOICES, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')

    is_verified = models.BooleanField(default=False)

    # REQUIRED AUTH FIELDS
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # email already required

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
    
    @property
    def username(self):
        return self.email
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
