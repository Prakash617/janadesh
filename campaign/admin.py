from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Campaign, CampaignActivity, Volunteer

# Register your models here.
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'start_date', 'end_date', 'status', 'is_featured', 'created_at', 'action_buttons')
    list_filter = ('status', 'is_featured', 'start_date', 'end_date')
    list_editable = ('status', 'is_featured')
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np')
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title_en', 'title_np', 'slug', 'banner', 'description_en', 'description_np', 'goal')
        }),
        ('Schedule & Location', {
            'fields': ('start_date', 'end_date', 'region_en', 'region_np')
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'created_by')
        }),
        # ('Dates', {
        #     'fields': ('created_at', 'updated_at'),
        #     'classes': ('collapse',)
        # }),
    )

    def action_buttons(self, obj):
        edit_url = reverse('admin:campaign_campaign_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

admin.site.register(Campaign, CampaignAdmin)

class CampaignActivityAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'campaign', 'activity_type', 'date', 'location_en', 'participants_count', 'created_at', 'action_buttons')
    list_filter = ('activity_type', 'campaign', 'date')
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np', 'location_en', 'location_np')
    date_hierarchy = 'date'
    exclude = ('created_at', 'updated_at')
    
    def action_buttons(self, obj):
        edit_url = reverse('admin:campaign_campaignactivity_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

admin.site.register(CampaignActivity, CampaignActivityAdmin)

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name','membership_type', 'email', 'phone', 'campaign', 'created_at', 'action_buttons')
    list_filter = ('campaign', 'membership_type')
    search_fields = ('name', 'email', 'phone', 'address', 'skills')
    # readonly_fields = ('created_at', 'updated_at')
    exclude = ('created_at', 'updated_at')

    def action_buttons(self, obj):
        edit_url = reverse('admin:campaign_volunteer_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

admin.site.register(Volunteer, VolunteerAdmin)
