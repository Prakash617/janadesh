from django.contrib import admin
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

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "organization")
    list_filter = ("organization",)
    search_fields = ("name",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "organization")
    list_filter = ("organization",)
    filter_horizontal = ("permissions",)


@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "assigned_at")
    list_filter = ("role",)
