from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Organization, Branch, Role, StaffRole



@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name_en",
        "name_np",
        "email",
        "phone",
        "established_date",
        "created_at",
        "action_buttons"
    )
    list_filter = ("established_date", "created_at")
    search_fields = ("name_en", "name_np", "email", "phone")
    prepopulated_fields = {"slug": ("name_en",)}
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "name_en",
                "name_np",
                "slug",
                "description_en",
                "description_np",
            )
        }),
        ("Media", {
            "fields": (
                "logo",
                "banner",
                "manifesto_document",
            )
        }),
        ("Manifesto Content", {
            "fields": (
                "manifesto_en",
                "manifesto_np",
            )
        }),
        ("Contact Information", {
            "fields": (
                "email",
                "phone",
                "website",
                "address_en",
                "address_np",
            )
        }),
        ("Social Links", {
            "fields": (
                "facebook",
                "twitter",
                "instagram",
                "youtube",
            )
        }),
        ("Dates", {
            "fields": (
                "established_date",
                "created_at",
                "updated_at",
            )
        }),
    )

    def action_buttons(self, obj):
        edit_url = reverse('admin:organization_app_organization_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "action_buttons")
    list_filter = ("organization",)
    search_fields = ("name",)

    def action_buttons(self, obj):
        edit_url = reverse('admin:organization_app_branch_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "action_buttons")
    list_filter = ("organization",)
    filter_horizontal = ("permissions",)

    def action_buttons(self, obj):
        edit_url = reverse('admin:organization_app_role_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'


@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "assigned_at", "action_buttons")
    list_filter = ("role",)

    def action_buttons(self, obj):
        edit_url = reverse('admin:organization_app_staffrole_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'
