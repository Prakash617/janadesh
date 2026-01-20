from django.contrib import admin
from django.urls import reverse
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
        "action_buttons"
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

    def action_buttons(self, obj):
        edit_url = reverse('admin:manifesto_manifesto_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'
