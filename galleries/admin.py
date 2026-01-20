from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Gallery, GalleryImage

# Register your models here.

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'is_featured', 'order', 'created_at', 'action_buttons')
    list_filter = ('is_featured',)
    list_editable = ('is_featured', 'order')
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np')
    prepopulated_fields = {'slug': ('title_en',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [GalleryImageInline]

    def action_buttons(self, obj):
        edit_url = reverse('admin:galleries_gallery_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

admin.site.register(Gallery, GalleryAdmin)

# GalleryImage does not need a separate admin registration as it's an inline
