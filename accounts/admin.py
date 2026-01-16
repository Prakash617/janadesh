from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "organization", "branch", "is_staff")
    list_filter = ("organization", "branch", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "province")}),
        ("Organization Info", {"fields": ("organization", "branch")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "password1",
                "password2",
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Auto-assign organization & branch when created by admin
        """
        if not change:  # creating new user
            if not obj.organization:
                obj.organization = request.user.organization

            if not obj.branch:
                obj.branch = request.user.branch

        super().save_model(request, obj, form, change)
