from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Timeline

# Register your models here.
class TimelineAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'title_en', 'is_milestone', 'order', 'created_at', 'action_buttons')
    list_filter = ('year', 'is_milestone')
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('year', 'month', 'title_en', 'title_np', 'description_en', 'description_np', 'image')
        }),
        ('Settings', {
            'fields': ('is_milestone', 'order')
        }),
        # ('Dates', {
        #     'fields': ('created_at', 'updated_at'),
        #     'classes': ('collapse',)
        # }),
    )

    def action_buttons(self, obj):
        edit_url = reverse('admin:timelines_timeline_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

admin.site.register(Timeline, TimelineAdmin)
