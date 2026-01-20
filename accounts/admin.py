from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "organization", "branch", "is_staff", "action_buttons")
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
                "password",
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

    def action_buttons(self, obj):
        edit_url = reverse('admin:accounts_user_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'
