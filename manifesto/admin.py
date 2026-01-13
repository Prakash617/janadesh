from django.contrib import admin
from django.utils.html import format_html
from .models import Manifesto


@admin.register(Manifesto)
class ManifestoAdmin(admin.ModelAdmin):
    # Columns displayed in the list view
    list_display = (
        "title",
        "slug",
        "status",
        "published_at",
        "created_at",
        "updated_at",
        "pdf_file_link",
    )

    # Editable fields in list view
    list_editable = ("status",)

    # Filters
    list_filter = ("status", "created_at", "published_at")

    # Searchable fields
    search_fields = ("title", "slug", "description")

    # Ordering
    ordering = ("-created_at",)

    # Fields in the add/edit form
    fieldsets = (
        (None, {
            "fields": (
                "title",
                "slug",
                "description",
                "pdf_file",
                "status"
            )
        }),
        # ("Publishing", {
        #     "fields": ("status", "published_at"),
        # }),
    )

    # Auto-populate slug from title
    prepopulated_fields = {"slug": ("title",)}

    # Read-only timestamps
    readonly_fields = ("created_at", "updated_at")

    # Display PDF file as a link in admin list
    def pdf_file_link(self, obj):
        if obj.pdf_file:
            return format_html(
                '<a href="{}" target="_blank">View PDF</a>', obj.pdf_file.url
            )
        return "-"
    pdf_file_link.short_description = "PDF File"
