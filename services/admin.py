from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Service

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'slug', 'is_active', 'order', 'created_at', 'action_buttons')
    list_filter = ('is_active',)
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np')
    prepopulated_fields = {'slug': ('title_en',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title_en', 'title_np', 'slug', 'icon', 'image', 'description_en', 'description_np')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def action_buttons(self, obj):
        edit_url = reverse('admin:services_service_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

admin.site.register(Service, ServiceAdmin)
