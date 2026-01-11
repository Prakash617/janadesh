from django.urls import path, include
from janadesh.api.router import router
from .views import NewsletterSubscriptionViewSet

app_name = 'newsletter-api-v1'



router.register(r'newsletter', NewsletterSubscriptionViewSet, basename='newsletter')

