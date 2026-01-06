from django.contrib import admin
from .models import NewsletterSubscription

# Register your models here.
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    readonly_fields = ('subscribed_at', 'unsubscribed_at')

admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
