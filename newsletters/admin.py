from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import NewsletterSubscription

# Register your models here.
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at', 'action_buttons')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    readonly_fields = ('subscribed_at', 'unsubscribed_at')

    def action_buttons(self, obj):
        edit_url = reverse('admin:newsletters_newslettersubscription_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
